# Task API (FastAPI)

Simple CRUD for tasks with validation; /health & /tasks endpoints.

> **Ethics/Safety**: Any security testing stays inside my own lab or with explicit permission.

## Getting Started
 python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) python main.py --help
EOP
elif [[ "fastapi" == "streamlit" ]]; then
  cat <<'EOP'
1) python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) streamlit run app.py
EOP
elif [[ "fastapi" == "flask" ]]; then
  cat <<'EOP'
1) python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) python app.py
EOP
elif [[ "fastapi" == "fastapi" ]]; then
  cat <<'EOP'
1) python3 -m venv .venv && source .venv/bin/activate
2) pip install -r requirements.txt
3) uvicorn app:app --reload
EOP
else
  echo "- Read the docs and tasks below."
fi )
