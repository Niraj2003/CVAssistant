from modules.generate_resume import resume_builder
from modules.generate_site import site_generator
from modules.resume_updator import info_updator


def main():
    job_description = """<JOB DESCRIPTION HERE>"""

    try:
        # Step 1: Update resume info with AI
        info_updator(job_description)

        # Step 2: Build updated resume (JSON → PDF/LaTeX)
        resume_builder()

        # Step 3: Generate portfolio site
        site_generator()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
