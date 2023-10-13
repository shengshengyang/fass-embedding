import os
from dotenv import load_dotenv
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

# Load environment variables
load_dotenv()

# Get SharePoint site and credentials
sharepoint_url = "https://dfrecyclecom.sharepoint.com"
username = os.getenv("SHAREPOINT_USERNAME")
password = os.getenv("SHAREPOINT_PASSWORD")

# Authenticate with SharePoint
auth_ctx = AuthenticationContext(sharepoint_url)
if auth_ctx.acquire_token_for_user(username, password):
    # Create client context
    ctx = ClientContext(sharepoint_url, auth_ctx)

    # Specify relative url of file
    relative_url = "/IT/Shared%20Documents/00.Public/AI%20%E7%9B%B8%E9%97%9C/ai_bot_data.xlsx"

    # Download file
    download_path = "./phone1.xlsx"
    file_content = File.open_binary(ctx, relative_url)
    with open(download_path, "wb") as local_file:
        local_file.write(file_content.content)

    print(f"File downloaded to: {download_path}")
else:
    print(auth_ctx.get_last_error())
