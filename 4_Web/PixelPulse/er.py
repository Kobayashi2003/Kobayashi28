from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy.orm import class_mapper
from app import create_app, db
from app.models import User, Image, Tag, Collection, Comment

# Create the Flask app
app = create_app()

# Use the application context
with app.app_context():
    # Create the graph
    graph = create_schema_graph(
        metadata=db.metadata,
        show_datatypes=False,
        show_indexes=False,
        rankdir='LR',
        concentrate=False,
        engine=db.engine
    )

    # Save the graph
    graph.write_png('erd_from_sqlalchemy.png')

print("ER diagram has been generated and saved as 'erd_from_sqlalchemy.png'")