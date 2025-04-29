import os
import pandas as pd

# Grade mapping for GPA calculation
GRADE_MAP = {
    "A": 4.00,
    "A-": 3.67,
    "B+": 3.33,
    "B": 3.00,
    "B-": 2.67,
    "C+": 2.33,
    "C": 2.00,
    "C-": 1.67,
    "D+": 1.33,
    "D": 1.00,
    "D-": 0.67,
    "F": 0.00,
    "I": None,
    "W": None,
    "P": None,
    "NP": None
}

class GPAProcessor:
    def __init__(self):
        # Separate dictionaries for different file types
        self.section_dfs = {}  # Keyed by section name from .sec files
        self.group_dfs = {}    # Keyed by file name from .grp files
        self.run_dfs = {}      # Keyed by file name from .run or .runthis files
        
        self.section_gpas = {}
        self.group_gpas = {}
        self.section_z_scores = {}  # New: store z-scores for sections
        self.group_z_scores = {}    # New: store z-scores for groups
        self.good_list = {}
        self.work_list = {}
        self.section_credit_hours = {}  # Store credit hours per section

        # These will store the original data for re-filtering on run selection
        self.all_section_dfs = {}
        self.all_group_dfs = {}
        self.student_history = {}  # Track students across good/work lists
    
    def reset_to_all_data(self):
        """
        Reset to show data from all runs by restoring all sections and groups from original data.
        """
        # Restore all groups and sections from original data
        self.group_dfs = self.all_group_dfs.copy()
        self.section_dfs = self.all_section_dfs.copy()
        
    def load_files_to_dataframes(self, directory):
        """
        Load all .run, .grp, .sec, and .runthis files from the specified directory.
        """
        self.section_dfs = {}
        self.group_dfs = {}
        self.run_dfs = {}
        
        # Include '.runthis' to catch files like "firstrun.runThis" (case-insensitive)
        extensions = ('.run', '.grp', '.sec', '.runthis')
        
        for file in os.listdir(directory):
            if file.lower().endswith(extensions):
                file_path = os.path.join(directory, file)
                file_name, ext = os.path.splitext(file)
                ext = ext.lower()
                try:
                    if ext == '.sec':
                        # Process section file
                        with open(file_path, 'r') as f:
                            header = f.readline().strip()  # First line header
                        header_parts = header.split()
                        section_name = header_parts[0]
                        # Extract credit hours if provided; default to 3.0 otherwise
                        credit_hours = float(header_parts[1]) if len(header_parts) > 1 else 3.0
                        self.section_credit_hours[section_name] = credit_hours
                        
                        df = pd.read_csv(file_path, sep=",", skiprows=1, header=None)
                        df = df.applymap(lambda x: x.replace('"', '').strip() if isinstance(x, str) else x)
                        df.columns = ["Name", "ID", "Grade"]
                        df['Numeric Grade'] = df['Grade'].map(GRADE_MAP)
                        self.section_dfs[section_name] = df
                    
                    elif ext == '.grp':
                        # Process group file
                        with open(file_path, 'r') as f:
                            group_name = f.readline().strip()  # First line is group name
                            sections = [line.strip() for line in f if line.strip()]
                        
                        normalized_sections = [s.replace('.SEC', '').replace('.sec', '') for s in sections]
                        df = pd.DataFrame({
                            'Group Name': [group_name] * len(normalized_sections),
                            'Section': normalized_sections
                        })
                        self.group_dfs[file_name] = df
                    
                    # Accept files that end with .run or .runthis
                    elif ext in ('.run', '.runthis'):
                        with open(file_path, 'r') as f:
                            semester = f.readline().strip()  # First line: semester info
                            groups = [line.strip() for line in f if line.strip()]
                        
                        normalized_groups = [g.replace('.grp', '').replace('.GRP', '') for g in groups]
                        df = pd.DataFrame({
                            'Semester': [semester] * len(normalized_groups),
                            'Group': normalized_groups
                        })
                        self.run_dfs[file_name] = df
                except Exception as e:
                    print(f"Could not read {file}: {e}")
                    raise
        
        # Save original copies for future run filtering
        self.all_section_dfs = self.section_dfs.copy()
        self.all_group_dfs = self.group_dfs.copy()
        
        return len(self.section_dfs) + len(self.group_dfs) + len(self.run_dfs)

    def calculate_all_gpas(self):
        """
        Calculate GPAs for all sections and groups.
        Section GPA remains as the simple mean (since all students in a section have the same credit hours).
        Group GPA is now calculated as a weighted average based on credit hours.
        """
        # Calculate section GPAs (simple average per section)
        for section_name, df in self.section_dfs.items():
            valid_grades = df[df['Numeric Grade'].notna()]
            if not valid_grades.empty:
                self.section_gpas[section_name] = valid_grades['Numeric Grade'].mean()
            else:
                self.section_gpas[section_name] = None
        
        # Calculate group GPAs using weighted averages
        for group_name, df in self.group_dfs.items():
            sections = df['Section'].tolist()
            total_points = 0.0
            total_credits = 0.0
            for section in sections:
                if section in self.section_dfs:
                    df_section = self.section_dfs[section]
                    credit_hours = self.section_credit_hours.get(section, 3.0)
                    valid = df_section[df_section['Numeric Grade'].notna()]
                    if not valid.empty:
                        total_points += valid['Numeric Grade'].sum() * credit_hours
                        total_credits += len(valid) * credit_hours
            self.group_gpas[group_name] = total_points / total_credits if total_credits > 0 else None
                        
        # Calculate z-scores after GPAs are calculated
        self.calculate_z_scores()
        
        return self.section_gpas, self.group_gpas

    def calculate_z_scores(self):
        """
        Calculate z-scores for sections and groups based on their GPAs.
        Z-score represents how many standard deviations a GPA is from the mean.
        """
        # Calculate z-scores for sections
        # Only consider sections that are currently in section_dfs (after filtering)
        filtered_section_gpas = [self.section_gpas[name] for name in self.section_dfs.keys() 
                               if name in self.section_gpas and self.section_gpas[name] is not None]
        
        # Reset section z-scores dictionary
        self.section_z_scores = {}
        
        if filtered_section_gpas:
            if len(filtered_section_gpas) == 1:
                # If there's only one section, z-score is 0
                for name in self.section_dfs.keys():
                    if name in self.section_gpas and self.section_gpas[name] is not None:
                        self.section_z_scores[name] = 0.0
            else:
                # Normal z-score calculation for multiple sections
                mean = sum(filtered_section_gpas) / len(filtered_section_gpas)
                std_dev = (sum((x - mean) ** 2 for x in filtered_section_gpas) / len(filtered_section_gpas)) ** 0.5
                
                if std_dev > 0:  # Avoid division by zero
                    for name in self.section_dfs.keys():
                        if name in self.section_gpas and self.section_gpas[name] is not None:
                            self.section_z_scores[name] = (self.section_gpas[name] - mean) / std_dev
                else:
                    # If all GPAs are the same, z-score is 0
                    for name in self.section_dfs.keys():
                        if name in self.section_gpas and self.section_gpas[name] is not None:
                            self.section_z_scores[name] = 0.0
        
        # Calculate z-scores for groups (keeping the fixed code we already provided)
        # Only consider groups that are currently in group_dfs (after filtering)
        filtered_group_gpas = [self.group_gpas[name] for name in self.group_dfs.keys() 
                              if name in self.group_gpas and self.group_gpas[name] is not None]
        
        # Reset group z-scores dictionary
        self.group_z_scores = {}
        
        if filtered_group_gpas:
            if len(filtered_group_gpas) == 1:
                # If there's only one group, z-score is 0
                for name in self.group_dfs.keys():
                    if name in self.group_gpas and self.group_gpas[name] is not None:
                        self.group_z_scores[name] = 0.0
            else:
                # Normal z-score calculation for multiple groups
                mean = sum(filtered_group_gpas) / len(filtered_group_gpas)
                std_dev = (sum((x - mean) ** 2 for x in filtered_group_gpas) / len(filtered_group_gpas)) ** 0.5
                
                if std_dev > 0:  # Avoid division by zero
                    for name in self.group_dfs.keys():
                        if name in self.group_gpas and self.group_gpas[name] is not None:
                            self.group_z_scores[name] = (self.group_gpas[name] - mean) / std_dev
                else:
                    # If all GPAs are the same, z-score is 0
                    for name in self.group_dfs.keys():
                        if name in self.group_gpas and self.group_gpas[name] is not None:
                            self.group_z_scores[name] = 0.0

    def populate_good_work_lists(self):
        """
        Create lists of students with A grades (Good List) and D/F grades (Work List).
        """
        self.good_list = {}
        self.work_list = {}
        
        for section_name, df in self.section_dfs.items():
            for _, student in df.iterrows():
                name, student_id, grade = student['Name'], student['ID'], student['Grade']
                if grade == 'A':   
                    if student_id in self.good_list:
                        self.good_list[student_id]['classes'].append(section_name)
                    else:
                        self.good_list[student_id] = {'name': name, 'classes': [section_name]}
                elif grade in ['F', 'D+', 'D', 'D-']:
                    if student_id in self.work_list:
                        self.work_list[student_id]['classes'].append(section_name)
                    else:
                        self.work_list[student_id] = {'name': name, 'classes': [section_name]}
        return self.good_list, self.work_list

    def get_grade_distribution(self, section_name):
        """
        Get the detailed grade distribution for a section.
        Returns a dictionary with keys:
          A, A-, B+, B, B-, C+, C, C-, D+, D, D-, and F.
        """
        if section_name not in self.section_dfs:
            return None
        df = self.section_dfs[section_name]
        grade_counts = df['Grade'].value_counts()
        distribution = {
            'A': grade_counts.get('A', 0),
            'A-': grade_counts.get('A-', 0),
            'B+': grade_counts.get('B+', 0),
            'B': grade_counts.get('B', 0),
            'B-': grade_counts.get('B-', 0),
            'C+': grade_counts.get('C+', 0),
            'C': grade_counts.get('C', 0),
            'C-': grade_counts.get('C-', 0),
            'D+': grade_counts.get('D+', 0),
            'D': grade_counts.get('D', 0),
            'D-': grade_counts.get('D-', 0),
            'F': grade_counts.get('F', 0)
        }
        return distribution

    def get_all_sections_data(self):
        """
        Get data for all sections for display.
        """
        sections_data = []
        for section_name, df in self.section_dfs.items():
            distribution = self.get_grade_distribution(section_name)
            section_data = {
                'name': section_name,
                'gpa': self.section_gpas.get(section_name),
                'z_score': self.section_z_scores.get(section_name),
                'distribution': distribution
            }
            sections_data.append(section_data)
        return sections_data

    def get_all_groups_data(self):
        """
        Get group data for display.
        """
        groups_data = []
        for group_name, df in self.group_dfs.items():
            sections = df['Section'].tolist()
            group_data = {
                'name': df['Group Name'].iloc[0] if 'Group Name' in df.columns else group_name,
                'gpa': self.group_gpas.get(group_name),
                'z_score': self.group_z_scores.get(group_name),
                'sections': sections
            }
            groups_data.append(group_data)
        return groups_data

    def get_overall_gpa(self):
        """
        Calculate the overall GPA across all sections using weighted averages.
        """
        total_points = 0.0
        total_credits = 0.0
        for section_name, df in self.section_dfs.items():
            credit_hours = self.section_credit_hours.get(section_name, 3.0)
            valid = df[df['Numeric Grade'].notna()]
            if not valid.empty:
                total_points += valid['Numeric Grade'].sum() * credit_hours
                total_credits += len(valid) * credit_hours
        return total_points / total_credits if total_credits > 0 else None

    def get_summary_statistics(self):
        """
        Get summary statistics using unique student IDs.
        """
        section_count = len(self.section_dfs)
        group_count = len(self.group_dfs)
        student_ids = set()
        for df in self.section_dfs.values():
            student_ids.update(df['ID'].unique())
        student_count = len(student_ids)
        return {
            'section_count': section_count,
            'group_count': group_count,
            'student_count': student_count,
            'good_list_count': len(self.good_list),
            'work_list_count': len(self.work_list),
            'overall_gpa': self.get_overall_gpa()
        }

    def select_run(self, run_file_name):
        """
        Filter group and section data based on the selected run file.
        This version resets the group and section data from the original copies,
        ensuring that each run selection starts with the full dataset.
        """
        if run_file_name not in self.run_dfs:
            raise ValueError(f"Run file '{run_file_name}' not found.")
        run_df = self.run_dfs[run_file_name]
        valid_groups = set(run_df['Group'].tolist())
        
        # Reset group and section data from original copies
        self.group_dfs = {key: df for key, df in self.all_group_dfs.items()
                          if df['Group Name'].iloc[0] in valid_groups}
        valid_sections = set()
        for df in self.group_dfs.values():
            valid_sections.update(df['Section'].tolist())
        self.section_dfs = {sec: df for sec, df in self.all_section_dfs.items() if sec in valid_sections}

    def export_section_data(self, filepath):
        """Export section data to a CSV file"""
        if not self.section_dfs:
            return False
            
        # Create a DataFrame with all section data for export
        export_data = []
        for section_name, df in self.section_dfs.items():
            distribution = self.get_grade_distribution(section_name)
            gpa = self.section_gpas.get(section_name)
            z_score = self.section_z_scores.get(section_name)
            row = {
                'Section Name': section_name,
                'GPA': gpa if gpa is not None else 'N/A',
                'Z-Score': z_score if z_score is not None else 'N/A'
            }
            # Add grade distribution
            for grade, count in distribution.items():
                row[grade] = count
                
            export_data.append(row)
        
        # Convert to DataFrame and export
        export_df = pd.DataFrame(export_data)
        export_df.to_csv(filepath, index=False)
        return True

    def export_group_data(self, filepath):
        """Export group data to a CSV file"""
        if not self.group_dfs:
            return False
            
        export_data = []
        for group_name, df in self.group_dfs.items():
            sections = df['Section'].tolist()
            gpa = self.group_gpas.get(group_name)
            z_score = self.group_z_scores.get(group_name)
            group_data = {
                'Group Name': df['Group Name'].iloc[0] if 'Group Name' in df.columns else group_name,
                'GPA': gpa if gpa is not None else 'N/A',
                'Z-Score': z_score if z_score is not None else 'N/A',
                'Sections': ', '.join(sections)
            }
            export_data.append(group_data)
        
        export_df = pd.DataFrame(export_data)
        export_df.to_csv(filepath, index=False)
        return True

    def export_student_list(self, filepath, list_type='good'):
        """Export good or work list to a CSV file"""
        student_list = self.good_list if list_type == 'good' else self.work_list
        if not student_list:
            return False
            
        export_data = []
        for student_id, info in student_list.items():
            student_data = {
                'Student Name': info['name'],
                'Student ID': student_id,
                'Classes': ', '.join(info['classes'])
            }
            export_data.append(student_data)
        
        export_df = pd.DataFrame(export_data)
        export_df.to_csv(filepath, index=False)
        return True

    def analyze_student_history(self):
        """
        Analyze students across sections to identify patterns:
        1. Students who appear on the good list multiple times
        2. Students who appear on the work list multiple times
        3. Students who appear on both good and work lists
        """
        repeat_good = {}
        repeat_work = {}
        mixed = {}
        
        # Track the good list and work list appearances by section
        student_appearances = {}
        
        # Process good list
        for student_id, info in self.good_list.items():
            if student_id not in student_appearances:
                student_appearances[student_id] = {
                    'name': info['name'],
                    'good_classes': set(info['classes']),
                    'work_classes': set()
                }
            else:
                student_appearances[student_id]['good_classes'].update(info['classes'])
        
        # Process work list
        for student_id, info in self.work_list.items():
            if student_id not in student_appearances:
                student_appearances[student_id] = {
                    'name': info['name'],
                    'good_classes': set(),
                    'work_classes': set(info['classes'])
                }
            else:
                student_appearances[student_id]['work_classes'].update(info['classes'])
        
        # Analyze the patterns
        for student_id, info in student_appearances.items():
            good_count = len(info['good_classes'])
            work_count = len(info['work_classes'])
            
            if good_count > 1 and work_count == 0:
                # Student appears on good list multiple times
                repeat_good[student_id] = {
                    'name': info['name'],
                    'classes': list(info['good_classes'])
                }
            
            if work_count > 1 and good_count == 0:
                # Student appears on work list multiple times
                repeat_work[student_id] = {
                    'name': info['name'],
                    'classes': list(info['work_classes'])
                }
            
            if good_count > 0 and work_count > 0:
                # Student appears on both good and work lists
                mixed[student_id] = {
                    'name': info['name'],
                    'good_classes': list(info['good_classes']),
                    'work_classes': list(info['work_classes'])
                }
        
        return {
            'repeat_good': repeat_good,
            'repeat_work': repeat_work,
            'mixed': mixed
        }

    def get_history_summary(self):
        """
        Create a summary of student history patterns.
        Returns a dictionary with student ID keys and flags for different patterns.
        """
        history_patterns = self.analyze_student_history()
        
        # Create a consolidated view for all students
        summary = {}
        
        # Process students with multiple A grades
        for student_id, info in history_patterns['repeat_good'].items():
            summary[student_id] = {
                'name': info['name'],
                'repeat_good': True,
                'repeat_work': False,
                'mixed': False
            }
        
        # Process students with multiple D/F grades
        for student_id, info in history_patterns['repeat_work'].items():
            if student_id in summary:
                summary[student_id]['repeat_work'] = True
            else:
                summary[student_id] = {
                    'name': info['name'],
                    'repeat_good': False,
                    'repeat_work': True,
                    'mixed': False
                }
        
        # Process students with mixed performance
        for student_id, info in history_patterns['mixed'].items():
            if student_id in summary:
                summary[student_id]['mixed'] = True
            else:
                summary[student_id] = {
                    'name': info['name'],
                    'repeat_good': False,
                    'repeat_work': False,
                    'mixed': True
                }
                
        return summary

    def export_history_data(self, filepath):
        """Export student history data to a CSV file"""
        history_summary = self.get_history_summary()
        if not history_summary:
            return False
            
        # Create export data
        export_data = []
        for student_id, info in history_summary.items():
            export_data.append({
                'Student Name': info['name'],
                'Student ID': student_id,
                'Good List Multiple Times': 'Yes' if info['repeat_good'] else 'No',
                'Work List Multiple Times': 'Yes' if info['repeat_work'] else 'No',
                'Both Lists': 'Yes' if info['mixed'] else 'No'
            })
        
        # Convert to DataFrame and export
        export_df = pd.DataFrame(export_data)
        export_df.to_csv(filepath, index=False)
        return True

    def get_student_gpa(self, student_id):
        """Calculate GPA for a specific student across all their sections"""
        total_points = 0.0
        total_credits = 0.0
        
        for section_name, df in self.section_dfs.items():
            student_row = df[df['ID'] == student_id]
            if not student_row.empty:
                numeric_grade = student_row['Numeric Grade'].iloc[0]
                if pd.notna(numeric_grade):  # Only count valid grades
                    credit_hours = self.section_credit_hours.get(section_name, 3.0)
                    total_points += numeric_grade * credit_hours
                    total_credits += credit_hours
        
        if total_credits > 0:
            return total_points / total_credits
        else:
            return None
