from backend import extract_text as e
from backend import analysis as a 
from backend import job_find as j
from backend import details as d
from backend import resumemaker as r
from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__, template_folder="html")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def format_to_html(text: str) -> str:
    lines = text.strip().split('\n')
    html_lines = ['<ul>']
    for line in lines:
        if line.strip().startswith('-'):
            html_lines.append(f"<li>{line.strip()[1:].strip()}</li>")
        elif line.strip():
            html_lines.append(f"<li>{line.strip()}</li>")
    html_lines.append('</ul>')
    return '\n'.join(html_lines)


@app.route("/")
def splash():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        job = request.form.get('job-description')
        resume = request.files.get('resume')

        if resume:
            file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
            resume.save(file_path)
            results = e.process_files(file_path)

            for result in results:
                text = result.cleaned_text

            if job:
                weakness = format_to_html(a.resume_weakness(text, job))
                improve = format_to_html(a.resume_improve(text, job))
                score = a.score(text)
                scores = a.scoring(text)
                job_links = j.search_jobs(job)
              
            else:
                weakness = format_to_html(a.resume_weakness(text))
                improve = format_to_html(a.resume_improve(text))
                score = a.score(text)
                scores = a.scoring(text)
                job_links = []
        

            print("All details are stored.")
            return render_template(
                "score_page.html",
                weakness=weakness,
                improve=improve,
                score=score,
                scores=scores,
                jobs=job_links
            )
        return "No file uploaded."

    return render_template("upload_page.html")


@app.route("/resume_maker")
def resume_maker():
    return render_template("form.html")



temp_resume_store = {}

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        summary = request.form['summary']

        resume_data = r.generate_resume(name, email, phone, summary)

        if not isinstance(resume_data, dict):
            return render_template('error.html', error_message="Failed to generate resume. Please try again.")

        temp_resume_store['latest'] = resume_data

        return redirect(url_for('select_template'))
    except Exception as e:
        return render_template('error.html', error_message=str(e))


@app.route('/select_template')
def select_template():
    return render_template('select_templates.html')

@app.route('/render_template/<template_name>')
def render_template_page(template_name):
    try:
        resume_data = temp_resume_store.get('latest')
        if not resume_data:
            return render_template('error.html', error_message="No resume data found. Please go back and submit the form.")

        template_map = {
            'classic': 'dynamicproffesionalblueprint.html',
            'professional': 'sleekmidnightelegance.html',
            'elegant': 'vibrantredaccent.html',
            'luxurious': 'elegantpurpleedge.html',
            'creative': 'goldenprofessionalglow.html',
            'modern': 'modertechhorizon.html'
        }

        if template_name not in template_map:
            return render_template('error.html', error_message="Invalid template selected.")

        return render_template(template_map[template_name], resume_data=resume_data)
    except Exception as e:
        return render_template('error.html', error_message=str(e))


@app.route('/error')
def error():
    return render_template('error.html', error_message="An unexpected error occurred.")

if __name__ == "__main__":
    app.run(debug=True)
