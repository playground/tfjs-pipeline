#! /usr/bin/env node
const {rename, readdir, copyFile, existsSync, mkdirSync, readFileSync} = require('fs');
const jsonfile = require('jsonfile');
const convert = require('xml-js');

const task = process.env.npm_config_task || 'rename_maximo_assets';

let build = {
  rename_maximo_assets: () => {
    const path = process.env.npm_config_path;
    if(!path) {
      build.exit('path is required, provide --path=...');
    }
    jsonfile.readFile(`${path}/prop.json`, (err, json) => {
      if (!err) {
        let fileInfo = JSON.parse(json['file_prop_info']);
        fileInfo.map((info) => {
          console.log(info['original_file_name']);
          let type = /\.[0-9a-z]{1,5}$/i.exec(info.original_file_name)[0];
          let name = info.original_file_name.replace(type, '');
          console.log(`${path}/${info._id}${type}`, `${path}/${info.original_file_name}`)
          console.log(`${path}/${info._id}.xml`, `${path}/${name}.xml`)
          rename(
            `${path}/${info._id}${type}`, 
            `${path}/${info.original_file_name}`,
            err => console.log(err));
          rename(
            `${path}/${info._id}.xml`, 
            `${path}/${name}.xml`,
            err => console.log(err));
        })
      } else {
        build.exit(err);
      }
    });  
  },
  partition_dataset: () => {
    const path = process.env.npm_config_path;
    if(!path) {
      build.exit('path is required, provide --path=...');
    }
    const train_ratio = process.env.npm_config_ratio || 0.9;
    readdir(path, (err, files) => {
      const assets = files.filter((file) => file.match(/jpg|png|gif|jpeg/i));
      const train_num = parseInt(assets.length * train_ratio);
      console.log(`total: ${assets.length}, train: ${train_num}, test: ${assets.length-train_num}`);
      if(!existsSync(`${path}/train`)) {
        mkdirSync(`${path}/train`)
      } else {
        build.exit('train directory already exists');
      }
      if(!existsSync(`${path}/test`)) {
        mkdirSync(`${path}/test`)
      } else {
        build.exit('test directory already exists');
      }
      assets.forEach((asset, i) => {
        console.log(asset, i)
        let type = /\.[0-9a-z]{1,5}$/i.exec(asset)[0];
        let name = asset.replace(type, '');
        let target = i < train_num ? 'train' : 'test';
        copyFile(`${path}/${asset}`, `${path}/${target}/${asset}`, (err) => console.log(err));
        copyFile(`${path}/${name}.xml`, `${path}/${target}/${name}.xml`, (err) => console.log(err));
      })
    });
  },
  xml_to_csv: () => {
    const path = process.env.npm_config_path;
    const origin = process.env.npm_config_origin;
    let xmls, xml;
    if(!path || !origin) {
      build.exit('path and orgin are required, provide --path=... --origin=...');
    }
    ['train', 'test'].forEach((target) => {
      const dir = `${path}/${target}`;
      readdir(dir, (err, files) => {
        xmls = files.filter((file) => file.indexOf('.xml') > 0);
        xmls.forEach((name, i) => {
          xml = readFileSync(`${dir}/${name}`);
          let json = JSON.parse(convert.xml2json(xml, {compact: true, space: 2}));
          console.log(json.annotation.object)
          let object = json.annotation.object;
          try {
            object.forEach((obj) => {
              // console.log(obj.name, obj.bndbox)
            })
           let csv = '';
           if(origin.toLowerCase() === 'maximo') {
             csv = 'filename,width,height,class,xmin,ymin,xmax,ymax\n';
 
           }
 
          } catch(e) {
            console.log(json.annotation, name)
            build.exit(name)
          }
        })
      })
    })

  },
  exit: (msg) => {
    console.log(msg);
    process.exit(0);
  }
}

build[task]();