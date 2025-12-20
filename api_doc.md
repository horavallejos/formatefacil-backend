Use Supabase with Python

Learn how to create a Supabase project, add some sample data to your database, and query the data from a Python app.

1
Create a Supabase project
Go to database.new and create a new Supabase project.

Alternatively, you can create a project using the Management API:

# First, get your access token from https://supabase.com/dashboard/account/tokens
export SUPABASE_ACCESS_TOKEN="your-access-token"
# List your organizations to get the organization ID
curl -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \
  https://api.supabase.com/v1/organizations
# Create a new project (replace <org-id> with your organization ID)
curl -X POST https://api.supabase.com/v1/projects \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "<org-id>",
    "name": "My Project",
    "region": "us-east-1",
    "db_pass": "<your-secure-password>"
  }'
When your project is up and running, go to the Table Editor, create a new table and insert some data.

Alternatively, you can run the following snippet in your project's SQL Editor. This will create a instruments table with some sample data.

-- Create the table
create table instruments (
  id bigint primary key generated always as identity,
  name text not null
);
-- Insert some sample data into the table
insert into instruments (name)
values
  ('violin'),
  ('viola'),
  ('cello');
alter table instruments enable row level security;
Make the data in your table publicly readable by adding an RLS policy:

create policy "public can read instruments"
on public.instruments
for select to anon
using (true);
2
Create a Python app with Flask
Create a new directory for your Python app and set up a virtual environment.

Terminal
mkdir my-app && cd my-app
python3 -m venv venv
source venv/bin/activate
3
Install Flask and the Supabase client library
The fastest way to get started is to use Flask for the web framework and the supabase-py client library which provides a convenient interface for working with Supabase from a Python app.

Install both packages using pip.

Terminal
pip install flask supabase
4
Create Environment Variables file
Create a .env file in your project root and populate it with your Supabase connection variables:

Project URL
formatefacil.online / FORMATE FACIL .ONLINE
https://eraprpohvuqawmxjczfi.supabase.co

Publishable key
formatefacil.online / FORMATE FACIL .ONLINE
sb_publishable_kiTMtJhRSMYZGPBUh_lzWg_ECdN3bHF

Anon key
formatefacil.online / FORMATE FACIL .ONLINE
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyYXBycG9odnVxYXdteGpjemZpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYwNDExMjAsImV4cCI6MjA4MTYxNzEyMH0.iTg8ANwTVPBJM_gm5cz9rMF17gCQjjDWFucoGhAx4U8

railway
formatefacil.online
3892bdde-ca26-45a9-91fc-b423ef0042cc

.env
SUPABASE_URL=<SUBSTITUTE_SUPABASE_URL>
SUPABASE_PUBLISHABLE_KEY=<SUBSTITUTE_SUPABASE_PUBLISHABLE_KEY>
You can also get the Project URL and key from the project's Connect dialog.

Changes to API keys
Supabase is changing the way keys work to improve project security and developer experience. You can read the full announcement, but in the transition period, you can use both the current anon and service_role keys and the new publishable key with the form sb_publishable_xxx which will replace the older keys.

In most cases, you can get the correct key from the Project's Connect dialog, but if you want a specific key, you can find all keys in the API Keys section of a Project's Settings page:

For legacy keys, copy the anon key for client-side operations and the service_role key for server-side operations from the Legacy API Keys tab.
For new keys, open the API Keys tab, if you don't have a publishable key already, click Create new API Keys, and copy the value from the Publishable key section.
Read the API keys docs for a full explanation of all key types and their uses.

5
Query data from the app
Install the python-dotenv package to load environment variables:

pip install python-dotenv
Create an app.py file and add a route that fetches data from your instruments table using the Supabase client.

app.py
import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_PUBLISHABLE_KEY")
)
@app.route('/')
def index():
    response = supabase.table('instruments').select("*").execute()
    instruments = response.data
    html = '<h1>Instruments</h1><ul>'
    for instrument in instruments:
        html += f'<li>{instrument["name"]}</li>'
    html += '</ul>'
    return html
if __name__ == '__main__':
    app.run(debug=True)
6
Start the app
Run the Flask development server, go to http://localhost:5000 in a browser and you should see the list of instruments.

Terminal
python app.py
Next steps#
Set up Auth for your app
Insert more data into your database
Upload and serve static files using Storage