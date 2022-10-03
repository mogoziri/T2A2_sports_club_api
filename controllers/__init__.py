from controllers.trainers_controller import trainers
from controllers.trainings_controller import trainings
from controllers.auth_controller import auth
from controllers.schedule_controller import schedule
from controllers.visits_controller import visit
from controllers.clients_controller import clients

registerable_controllers = [trainings, trainers, auth, schedule, visit, clients]
