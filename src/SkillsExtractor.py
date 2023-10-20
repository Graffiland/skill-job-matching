import re
import yaml

class SkillsExtractor:

    def __init__(self,jobs_skills_config_path ):
        self.jobs_skills_config_path = jobs_skills_config_path
        try:
                # Load the YAML file
                with open(jobs_skills_config_path, 'r') as file:
                    self.JOBS_SKILLS_CONFIG = yaml.safe_load(file)

        except IOError:
                print(f"Error attempting to open the jobs skills config path: {jobs_skills_config_path}")

    def extract_skills(self, cv_redacted_text):
        skills_list = []
        for skills_group_dict in self.JOBS_SKILLS_CONFIG:
            for skills_group_name, skills in skills_group_dict.items():
                set_of_skills =self.extract_skills_helper(cv_redacted_text, skills)
                skills_list.append((skills_group_name,set_of_skills))
        return skills_list

    def term_count(self, string_to_search, term):
        """
        A utility function which counts the number of times `term` occurs in `string_to_search`
        :param string_to_search: A string which may or may not contain the term.
        :type string_to_search: str
        :param term: The term to search for the number of occurrences for
        :type term: str
        :return: The number of times the `term` occurs in the `string_to_search`
        :rtype: int
        """
        try:
            regular_expression = re.compile(term, re.IGNORECASE)
            result = re.findall(regular_expression, string_to_search)
            return len(result)
        except Exception:
            print('Error occurred during regex search')
            return 0

    def extract_skills_helper(self, resume_text, skills):
        potential_skills_dict = dict()
        matched_skills = set()

        # TODO This skill input formatting could happen once per run, instead of once per observation.
        for skill_input in skills:

            # Format list inputs
            if type(skill_input) is list and len(skill_input) >= 1:
                potential_skills_dict[skill_input[0]] = skill_input

            # Format string inputs
            elif type(skill_input) is str:
                potential_skills_dict[skill_input] = [skill_input]
            else:
                print('Unknown skill listing type: {}. Please format as either a single string or a list of strings'
                            ''.format(skill_input))

        for (skill_name, skill_alias_list) in potential_skills_dict.items():

            skill_matches = 0
            # Iterate through aliases
            for skill_alias in skill_alias_list:
                # Add the number of matches for each alias
                skill_matches += self.term_count(resume_text, skill_alias.lower())

            # If at least one alias is found, add skill name to set of skills
            if skill_matches > 0:
                matched_skills.add(skill_name)

        return matched_skills

