import json

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API keys
load_dotenv()


def info_updator(job_desc: str):
    # Read prompt from external file
    with open("prompts/cv_updator_prompt_v1.txt", "r") as f:
        template_str = f.read()

    job_description = job_desc  # assuming you have this already

    # Create PromptTemplate
    prompt = PromptTemplate(
        input_variables=["resume_json", "job_description"],
        template=template_str,
    )

    # Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    # Build chain
    chain = prompt | llm

    # Load resume JSON
    with open('data/info.json', encoding='utf-8') as f:
        r_data = json.load(f)

    resume_data = {key: r_data[key] for key in ["summary", "skills", "work_experience", "projects"] if key in r_data}

    # Run chain
    updated_resume = chain.invoke({
        "resume_json": json.dumps(resume_data, indent=2),
        "job_description": job_description
    })

    # Clean Gemini output (remove ```json ... ``` wrappers if present)
    raw_output = updated_resume.content.strip()
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")  # remove backticks
        raw_output = raw_output.replace("json\n", "", 1).replace("json\r\n", "", 1)

    # Parse JSON safely
    try:
        updated_resume_json = json.loads(raw_output)
    except json.JSONDecodeError:
        print("Model returned invalid JSON. Here’s the raw output:")
        print(raw_output)
        raise ValueError("Invalid JSON returned from model.")
    else:
        for key in ["summary", "skills", "work_experience", "projects"]:
            if key in updated_resume_json:
                r_data[key] = updated_resume_json[key]
        # Save back to the same file
        with open("data/info.json", "w", encoding="utf-8") as f:
            json.dump(r_data, f, indent=2, ensure_ascii=False)
    print("Resume updated successfully with relevant skills and projects.")

