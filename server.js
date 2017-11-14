const express = require('express')
    const app = express()
    const exec = require('exec')

    app.use(function(req, res, next) {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            next();
        });

    app.get('/', (req, res) => {
            var data;

            exec(['tail', '-40', './bitcoinSentiment.csv'], function(err, out, code) {


                    if (err instanceof Error)
                        throw err;
                    data = out.split('\n')
                        data = data.map(d => d.split(','))
                        data = data.filter(d => d.length == 5)
                        return res.json(data);
                });

        })

    app.listen(3000, () => console.log('Example app listening on port 3000!'))

