from app import db

"""Utils: Executes the routine tasks that are operated on the applicatons database
to save delete and check for empty datasets/ """

def save(target):
	db.session.add(target)
	db.session.commit()

def delete(target):
	db.session.delete(target)
	db.session.commit()

def is_not_empty(*args):

	return all(len(value)> 0 for value in args)