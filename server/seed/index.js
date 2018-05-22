let py = spawn('python', ['selen.py'])
py.stdout.on('data', data => {
  console.log(data.toString())
})