#      0: "nose",
#      1: "left_eye",
#      2: "right_eye",
#      3: "left_ear",
#      4: "right_ear",
#      5: "left_shoulder",
#      6: right_shoulder",
#      7: "left_elbow",
#      8: "right_elbow",
#      9: "left_wrist",
#      10: "right_wrist",
#      11: "left_hip",
#      12: "right_hip",
#      13: "left_knee",
#      14: "right_knee",
#      15 : "left_ankle",
#      16 : "right_ankle",
#      17: "neck"

import jetson.inference
import jetson.utils

import argparse
import sys

# parse the command line
parser = argparse.ArgumentParser(description="Run pose estimation DNN on a video/image stream.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.poseNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="csi://0", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="resnet18-body", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="links,keypoints", help="pose overlay flags (e.g. --overlay=links,keypoints)\nvalid combinations are:  'links', 'keypoints', 'boxes', 'none'")
parser.add_argument("--threshold", type=float, default=0.15, help="minimum detection threshold to use") 

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

print(sys.argv)

net = jetson.inference.poseNet(opt.network, sys.argv, opt.threshold)

inputStream = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
outputStream = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

while True:
    img = inputStream.Capture()

    poses = net.Process(img, overlay=opt.overlay)
    skeletons = []

    for i in range(len(poses)):
        skeleton = {}
        skeleton['id'] = i
        skeleton['pose'] = poses[i]
        skeletons.append(skeleton)

    outputStream.Render(img)
    
    if(len(skeletons) < 2):
        print(skeletons)
    else:
        print(skeletons([0]))

    if not inputStream.IsStreaming() or not outputStream.IsStreaming():
        break
