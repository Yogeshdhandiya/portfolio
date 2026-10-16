# run_minimal.sh <vdir> <duration> <prescale> <outname>  (vdir has src/footage.mp4, plan.json, overlay/front.html; set ASSETS)
set -e
S=$(cd "$(dirname "$0")" && pwd)
V=$1; D=$2; PRE=$3; OUT=$4
VB=$(python3 -c "print(min(5200, int((28.5e6*8/$D - 160e3)/1000)))")
cd $V
ffmpeg -v error -y -i src/footage.mp4 -t $D -c copy src/trim.mp4
(cd overlay && npx @veedstudio/openedit-cli render front.html --out front.mov --fps 24000/1001 --duration $D --transparent --workers 3 > render.log 2>&1) &
python3 -I $S/audio.py src/trim.mp4 plan.json ${ASSETS:?set ASSETS to the sfx/music assets dir} mix.wav > audio.log 2>&1
wait
PRESCALE=$PRE GRADE_PRESET=blueglow python3 -I $S/compose.py src/trim.mp4 plan.json overlay/front.mov none matte_none mix.wav master.mp4 16 > build.log 2>&1
ffmpeg -v error -y -i master.mp4 -c:v libx264 -preset slow -b:v ${VB}k -pass 1 -passlogfile p2 -an -f mp4 /dev/null
ffmpeg -v error -y -i master.mp4 -c:v libx264 -preset slow -b:v ${VB}k -pass 2 -passlogfile p2 -c:a aac -b:a 160k -movflags +faststart $OUT
python3 -I $S/qa.py plan.json overlay/front.mov $OUT > qa.log 2>&1 || true
N=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 $OUT)
ffmpeg -v error -y -i $OUT -vf "select='not(mod(n\,$((N/12))))',scale=180:-1,tile=6x2" -frames:v 1 -vsync 0 sheet.jpg
rm -f overlay/front.mov.render -r
echo RUNDONE $(stat -c %s $OUT)
