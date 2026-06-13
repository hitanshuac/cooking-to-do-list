import getpass

from huggingface_hub import HfApi


def deploy():
    print("🚀 Hugging Face Space Auto-Deployment Script")
    print("This will create a public Hugging Face Space and upload your app.")

    token = getpass.getpass("Enter your Hugging Face Access Token (Write permissions): ")
    username = input("Enter your Hugging Face Username: ").strip()
    repo_name = input("Enter a name for your Space (e.g. Micro-Cooking-Planner): ").strip()

    if not username or not repo_name:
        print("Username and Space Name cannot be empty.")
        return

    repo_id = f"{username}/{repo_name}"
    api = HfApi(token=token)

    print(f"\n[1/2] Creating Space: {repo_id}...")
    try:
        api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="streamlit", exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating space: {e}")
        return

    print("[2/2] Uploading codebase (app.py, requirements.txt)...")
    try:
        api.upload_file(path_or_fileobj="app.py", path_in_repo="app.py", repo_id=repo_id, repo_type="space")
        api.upload_file(
            path_or_fileobj="requirements.txt", path_in_repo="requirements.txt", repo_id=repo_id, repo_type="space"
        )

        print("\n✅ Deployment Successful!")
        print(f"🔗 Your working link for submission: https://huggingface.co/spaces/{repo_id}")
        print("\n⚠️ IMPORTANT NEXT STEP: Your app will fail until you provide the API Key to Hugging Face!")
        print(f"1. Go to https://huggingface.co/spaces/{repo_id}/settings")
        print("2. Scroll down to 'Variables and secrets'")
        print("3. Click 'New secret'")
        print("4. Name: GEMINI_API_KEY")
        print("5. Value: <paste your actual Gemini key here>")
    except Exception as e:
        print(f"❌ Upload failed: {e}")


if __name__ == "__main__":
    deploy()
