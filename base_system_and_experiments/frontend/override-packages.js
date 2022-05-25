const fs = require('fs');
const mv = require('mv');
const fromPath = '/app/src/lib/packages/';
const toPath = '/node_modules/';

(function linkCustomPackage(_fromPath, _toPath) {
    let dirs;
    try {
        dirs = fs.readdirSync(_fromPath, { withFileTypes: true })
            .filter(dirent => dirent.isDirectory())
            .map(dirent => dirent.name)
    } catch {
        dirs = [];
    }

    dirs.forEach(dir => {
        const customPackagePath = _fromPath+dir;
        const symlinkPath = _toPath+dir;
        const stashPath = _toPath+'_'+dir;

        if(fs.existsSync(customPackagePath+'/package.json')){
            if(fs.existsSync(stashPath)){
                console.log(stashPath+' exists; skipping.');
            } else {
                mv(symlinkPath, stashPath, { mkdirp: true }, function(err){
                    if(!err){
                        console.log('stashing '+symlinkPath+' to '+stashPath);
                        fs.symlinkSync(customPackagePath, symlinkPath);
                        console.log('linking '+customPackagePath+' to '+symlinkPath);
                    } else {
                        console.log('error stashing '+symlinkPath+' to '+stashPath);
                        console.log(err)
                    }
                });
            }
        } else {
            try { fs.mkdirSync(symlinkPath); } catch {}
            linkCustomPackage(customPackagePath+'/', symlinkPath+'/');
        }
    });
})(fromPath, toPath, 1);
