const https = require('https');
const fs = require('fs');
const express = require('express');
const handlebars = require('handlebars');
const app = express();
const port = 3000;

const TIME_PERIODS = {
	_5m : '5m',
	_1h : '1h',
	_6h : '6h',
	_24h : '24h',
}

const headers = {
    'User-Agent': 'Personal ge tracker',
    'From': 'jackjordanyoung@gmail.com'
}

const hostname = 'prices.runescape.wiki';

async function apiGetRequest(path) {
	var options = {
		hostname: hostname,
		port: 443,
		path: path,
		method: 'GET',
		headers: headers
	};
	return new Promise((resolve, reject) => {
		req = https.request(options, (res) => {
			var body = '';
	
			res.on('data', function(chunk){
				body += chunk;
			});
	
			res.on('end', function(){
				resolve(JSON.parse(body));
			});
		});

		req.on('error', (err) => {
			reject(err)
		});
	
		req.end();
	})
}

async function getLatestPrices() {
	return (await apiGetRequest('/api/v1/osrs/latest')).data;
}

async function getMappings() {
	var mappings = {};
	for(const entry of await apiGetRequest('/api/v1/osrs/mapping')) mappings[entry['id']] = entry;
	return mappings
}

async function getPeriod(period) {
	return apiGetRequest(`/api/v1/osrs/${period}`);
}

async function getItemTimeSeries(period, id) {
	return apiGetRequest(`/api/v1/osrs/timeseries?timestep=${period}&id=${id}`);
}

async function getCompiledHtml(fileName) {
	return new Promise((resolve, reject) => {
		fs.readFile(`./html/${fileName}.html`, function (err, html) {
			if (err) {
				reject(err);
			}
			resolve(handlebars.compile(html.toString()));
		});
	})
}

const mappings = getMappings();

app.get('/', (req, res) => {
	res.send('Hello World!');
})

app.get('/test', async (req, res) => {
	res.status(200);
	res.setHeader('Content-Type', 'application/json');
	res.send(await getMappings());
})

app.get('/list', async (req, res) => {
	res.status(200);
	res.setHeader('Content-Type', 'text/html');

	var mappings = await getMappings();

	var test = await getLatestPrices();

	console.log(test);

	var args = {data : {}}
	for (let [key, value] of Object.entries(await getLatestPrices())) {
		args.data[key] = {
			latest : value,
			mappings : mappings[key]
		}
	}

	res.send((await getCompiledHtml('list'))(args));
	// res.setHeader('Content-Type', 'application/json');
	// res.send(await getLatestPrices());
})
//127.0.0.1:3000/item/4151
app.get('/item/:id', async (req, res) => {
	res.status(200);
	res.setHeader('Content-Type', 'application/json');
	res.send(await getItemTimeSeries(TIME_PERIODS._24h, req.params.id));
})

app.listen(port, () => {
	console.log(`Example app listening on port ${port}`);
})
