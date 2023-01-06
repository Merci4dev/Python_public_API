from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

# setting the votes url and prefix
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# votes decorator and prefix
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Votes, db: Session = Depends(database.get_db), current_user: str = Depends(oauth2.get_current_user)):


    # Checking if the vote allredy exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # Error por si el post no existe
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {vote.post_id} do not exitst")
    

    # Sentencia para encontrar un like
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, 
        models.Votes.user_id == current_user.id 
        )

    found_vote = vote_query.first()

    # Si el user provide una direcion 1 has esto:
    if (vote.dir == 1):
        # si el user quiere dar like al post pero este ya ha dido encontrado, este no podra votarlo otra  ves mas
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has alredy voted this post {vote.post_id}")

        #pero si no se ha votado sobre este pos entonces:
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added Vote"}

    else:
        #Pero si el user provide una direcion 0 has esto:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote do not exist")

        # Pero si se encuentra un vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted Vote"}