def build_semantic_representation(job):
  title = job.get("title", "")
  description = job.get("description", "")
  location = job.get("location", "")
  experience_level = job.get("experience_level", "")
  tech_stack = job.get("tech_stack", [])
  tech_stack_str = ", ".join(tech_stack)
  semantic_text = f"""
    Job Title: {title}
Experience Level: {experience_level}
Location: {location}
Tech Stack: {tech_stack_str}
Description: {description}
    """
  return semantic_text.strip()