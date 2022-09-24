from typing import List, Union
from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

import os
import requests
from typing import Dict, List
from dotenv import load_dotenv
from models import Tag
load_dotenv(".env")

AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.environ.get("AIRTABLE_TABLE_NAME")
AIRTABLE_TAGS_TABLE_NAME = os.environ.get("AIRTABLE_TAGS_TABLE_NAME")
AIRTABLE_TAG_GROUPS_TABLE_NAME = os.environ.get("AIRTABLE_TAG_GROUPS_TABLE_NAME")

endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TAGS_TABLE_NAME}'
group_endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TAG_GROUPS_TABLE_NAME}'
project_endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post('/tag', status_code = status.HTTP_201_CREATED, tags = ['tags'])
# def create(request: schemas.Tag, db: Session = Depends(get_db)):
#     new_tag = models.Tag(name = request.name, group_id = 12) # need to change
#     db.add(new_tag)
#     db.commit()
#     db.refresh(new_tag)
#     return new_tag
@app.post('/tag', status_code = status.HTTP_201_CREATED, tags = ['tags'])
def create(name, description):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    data = {
         "records": [
            {
                "fields": {
                    "Name": name,
                    "Description": description
                }
            }
        ]
    }
    r = requests.post(endpoint, json = data, headers = headers)
    return r.json()

# @app.delete('/tag/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['tags'])
# def destroy(id, db: Session = Depends(get_db)):
#     tag = db.query(models.Tag).filter(models.Tag.id == id)
#     if not tag.first():
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag with the id {id} is not found")
#     tag.delete(synchronize_session = False)
#     db.commit()
#     return 'Tag with the id ' + id + ' is deleted successfully'
@app.delete('/tag/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['tags'])
def destroy(id):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.delete(f"{endpoint}/{id}", headers = headers)
    if not r.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag with the id {id} is not found")
    return 'Tag with the id ' + id + ' is deleted successfully' 

# # @app.put('/tag/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['tags'])
# # def update(id, request: schemas.Tag, db: Session = Depends(get_db)):
# #     tag = db.query(models.Tag).filter(models.Tag.id == id)
# #     if not tag.first():
# #         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag with the id {id} is not found")
# #     tag.update({'name': request.name})
# #     db.commit()
# #     return 'Tag with the id ' + id + ' is updated successfully'
# @app.put('/tag/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['tags'])
# def update(id, changes: Dict[str, dict]):
#     """Takes a dictionary with keys of project ids and values of dictionaries with fields as keys and their updated values as values.
#     Updates the given fields."""

#     headers = {
#         "Authorization": f"Bearer {AIRTABLE_API_KEY}"
#     }

#     records: List[dict] = []
#     for id, change_dict in changes:
#         fields = change_dict.keys()
#         records.append(
#             {
#                 "id": id,
#                 "fields": {field:change_dict[field] for field in fields}
#             }
#         )
#     data = {
#         "records": records
#     }

#     r = requests.patch(endpoint, json = data, headers = headers)
#     return r.json()


# @app.get('/tag', response_model = List[schemas.ShowTag], tags = ['tags'])
# def all(db: Session = Depends(get_db)):
    # tags = db.query(models.Tag).all()
    # return tags
@app.get('/tag', tags = ['tags'])
def all():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.get(endpoint, headers = headers)
    return r.json()

# @app.get('/tag/{id}', status_code = 200, response_model = schemas.ShowTag, tags = ['tags'])
# def show(id, response: Response, db: Session = Depends(get_db)):
#     tag = db.query(models.Tag).filter(models.Tag.id == id).first()
#     if not tag:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag with the id {id} is not available")
#     return tag
@app.get('/tag/{id}', status_code = 200, tags = ['tags'])
def show(id, response: Response):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.get(f"{endpoint}/{id}", headers = headers)
    if not r:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag with the id {id} is not available")
    return r.json()



# @app.post('/tag_group', status_code = status.HTTP_201_CREATED, tags = ['tag_groups'])
# def create(request: schemas.TagGroup, db: Session = Depends(get_db)):
#     new_tag_group = models.TagGroup(name = request.name)
#     db.add(new_tag_group)
#     db.commit()
#     db.refresh(new_tag_group)
#     return new_tag_group
@app.post('/tag_group', status_code = status.HTTP_201_CREATED, tags = ['tag_groups'])
def create(name, description):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    data = {
         "records": [
            {
                "fields": {
                    "Name": name,
                    "Description": description
                }
            }
        ]
    }
    r = requests.post(group_endpoint, json = data, headers = headers)
    return r.json()

# @app.delete('/tag_group/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['tag_groups'])
# def destroy(id, db: Session = Depends(get_db)):
#     tag_group = db.query(models.TagGroup).filter(models.TagGroup.id == id)
#     if not tag_group.first():
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"TagGroup with the id {id} is not found")
#     tag_group.delete(synchronize_session = False)
#     db.commit()
#     return 'TagGroup with the id ' + id + ' is deleted successfully'
@app.delete('/tag_group/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['tag_groups'])
def destroy(id):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.delete(f"{group_endpoint}/{id}", headers = headers)
    if not r:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"TagGroup with the id {id} is not found")
    return 'Tag with the id ' + id + ' is deleted successfully' 

# @app.put('/tag_group/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['tag_groups'])
# def update(id, request: schemas.TagGroup, db: Session = Depends(get_db)):
#     tag_group = db.query(models.TagGroup).filter(models.TagGroup.id == id)
#     if not tag_group.first():
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"TagGroup with the id {id} is not found")
#     tag_group.update({'name': request.name})
#     db.commit()
#     return 'TagGroup with the id ' + id + ' is updated successfully'

# @app.get('/tag_group', response_model = List[schemas.ShowTagGroup], tags = ['tag_groups'])
# def all(db: Session = Depends(get_db)):
#     tag_groups = db.query(models.TagGroup).all()
#     return tag_groups
@app.get('/tag_group', tags = ['tag_groups'])
def all():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.get(group_endpoint, headers = headers)
    return r.json()

# @app.get('/tag_group/{id}', status_code = 200, response_model = schemas.ShowTagGroup, tags = ['tag_groups'])
# def show(id, response: Response, db: Session = Depends(get_db)):
#     tag_group = db.query(models.TagGroup).filter(models.TagGroup.id == id).first()
#     if not tag_group:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"TagGroup with the id {id} is not available")
#     return tag_group
@app.get('/tag_group/{id}', status_code = 200, tags = ['tag_groups'])
def show(id, response: Response):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    r = requests.get(f"{group_endpoint}/{id}", headers = headers)
    if not r:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Tag Group with the id {id} is not available")
    return r.json()



@app.post('/tag_group', status_code = status.HTTP_201_CREATED, tags = ['tag_groups'])
def create(name, description):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    data = {
         "records": [
            {
                "fields": {
                    "Name": name,
                    "Description": description
                }
            }
        ]
    }
    r = requests.post(group_endpoint, json = data, headers = headers)
    return r.json()

@app.post('/project', status_code = status.HTTP_201_CREATED, tags = ['projects'])
def create_project(name, description, region):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }

    data = {
         "records": [
            {
                "fields": {
                    "Name": name,
                    "Description": description,
                    "Region": region
                }
            }
        ]
    }

    r = requests.post(project_endpoint, json = data, headers = headers)
    return r.json()

# @app.delete(f'/project/{id}', status_code = status.HTTP_204_NO_CONTENT, tags = ['projects'])
# def remove_project(project: pr):
#     id = pr.get_id(project)
#     airtable.remove_project(id)
#     return f"Project with id {id} has been deleted successfully"

# @app.put(f'/project/{id}', status_code = status.HTTP_202_ACCEPTED, tags = ['projects'])
# def update(id, changes: dict):
#     project = get_project(id)
#     if not project:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Project with the id {id} is not found")
#     airtable.update_projects_put(id, pr.get_name(project), pr.get_description(project), pr.get_region(project), pr.get_primary_contact(project))
#     return f"Project with id {id} has been updated successfully"

# @app.get('/project', response_model = List[pr], tags = ['project'])
# def get_projects_list() -> List[pr]:
#     data = airtable.get_projects()["records"]
#     projects: List[pr] = []
#     for project in data:
#         fields = project["fields"]
#         # date created requires some scraping, as the airtable keeps more precise time than we need.
#         year, month, day = [int(string) for string in re.split(r'-', project["createdTime"][0:10])]
#         date = datetime(year, month, day)
#         projects.append(pr(project["id"], fields.get("Name", None), fields.get("Tags", None), fields.get("Description", None), date, fields.get("Region", None), fields.get("Primary_Contact", None)))
#     return projects

# @app.get(f'/project/{id}', status_code = 200, response_model = pr, tags = ['projects'])
# def get_project(id):
#     project = airtable.get_project(id)
#     if not project:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Project with the id {id} is not available")
#     fields = project["fields"]
#     year, month, day = [int(string) for string in re.split(r'-', project["createdTime"][0:10])]
#     date = datetime(year, month, day)
#     return pr(project["id"], fields.get("Name", None), fields.get("Tags", None), fields.get("Description", None), date, fields.get("Region", None), fields.get("Primary_Contact", None))
