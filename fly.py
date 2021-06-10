# from flight_routines.FaceTracking import FaceTrac
import sys
from flight_routines import FaceTracking, FaceTracking_V2



# if __name__=='__main__':
#     FaceTrack().track()


if len(sys.argv) != 2:
    raise ValueError('Please provide the name of the flight routine you wisb to execute. Options are `FaceTracking, `FaceTracking_V2`')

print(f'Script Name is {sys.argv[0]}')
routine = sys.argv[1]
if routine == 'FaceTracking':
    FaceTracking.FaceTrack().track()
elif routine == 'FaceTracking_V2':
    FaceTracking_V2.FaceTrack().track()