let app = require('express')();
let {spawn} = require("child_process");
let AWS = require('aws-sdk');
let uuid = require('uuid/v1');
let mongoose = require("mongoose");
let bodyParser = require("body-parser");
let cors = require("cors");
let lugage = require("./lugage");
let keys = require('./config/dev');
app.use(cors());
let s3 = new AWS.S3({
  signatureVersion: 'v4',
  region: 'ap-south-1',
  accessKeyId: keys.accessKeyId,
  secretAccessKey: keys.secretAccessKey
});
app.set('view engine','ejs');
app.use(bodyParser.json());
mongoose.connect("", {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

app.get('/',(req,res)=>{
  res.render('index');
});

app.post('/upload', (req, res) => {
  let dataToSend;
  const python = spawn('python', ['./validator.py ', req.body.passport.passportScannedFile])
  python.stdout.on('data', function(data) {
    dataToSend = data.toString();
    console.log(dataToSend);
  })
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    res.send({msg: "done"});
  })
  // lugage.create(req.body)
  // .then(l => {
  //   res.send({msg: "The details were successfully uploaded."});
  // })
  // .catch(() => {
  //   res.send({msg: "There was an error."});
  // });
})

app.get('/aws/upload',(req, res)=>{
  const key = `images/abhay.jpg`//`images/${uuid()}.jpg`;
  s3.getSignedUrl('putObject',{
    Bucket: 'knowledgemanagementsystem',
    ContentType: 'image/jpeg',
    Key: key
  },(err, url)=>{
    res.send({key,url});
  })
});

app.listen(8083);
