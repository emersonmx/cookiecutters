from invoke import Collection

from tasks import projects

ns = Collection()
ns.add_collection(projects)
