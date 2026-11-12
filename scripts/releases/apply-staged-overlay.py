"""Apply an exact, verified revision to a dedicated copied staging checkout only."""
import hashlib,json,os,pathlib,stat,subprocess,sys,tempfile
stage=pathlib.Path(sys.argv[1]).resolve(); revision=sys.argv[2]
if not stage.name.startswith('.myagent-keyword-stage-'):raise SystemExit('Dedicated staging directory required')
def git(*args):return subprocess.check_output(['git','-C',str(stage),*args])
revision=git('rev-parse','--verify',revision+'^{commit}').decode().strip()
manifest=json.loads(git('show',revision+':scripts/releases/2026-11-12-seo-overlay.json'))
pending=[]
for c in manifest['files']:
 rel=pathlib.PurePosixPath(c['path']);assert not rel.is_absolute() and '..' not in rel.parts
 path=stage.joinpath(*rel.parts);assert path.resolve().is_relative_to(stage) and not path.is_symlink()
 if c['base_sha256'] is None:assert not path.exists(),'Unexpected file: '+str(rel);mode=0o644
 else:
  assert path.is_file(),'Missing base: '+str(rel)
  assert hashlib.sha256(path.read_bytes()).hexdigest()==c['base_sha256'],'BASE HASH MISMATCH: '+str(rel)
  mode=stat.S_IMODE(path.stat().st_mode)
 target=git('show',revision+':'+str(rel));assert hashlib.sha256(target).hexdigest()==c['sha256'],'TARGET HASH MISMATCH: '+str(rel)
 pending.append((path,target,mode))
print('All bases and reviewed target bytes verified:',len(pending),flush=True)
for path,data,mode in pending:
 path.parent.mkdir(parents=True,exist_ok=True);fd,temp=tempfile.mkstemp(prefix='.seo-patch-',dir=path.parent)
 with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.chmod(temp,mode);os.replace(temp,path)
assert all(hashlib.sha256((stage/c['path']).read_bytes()).hexdigest()==c['sha256'] for c in manifest['files'])
print('PASS exact stage overlay. Live untouched. Revision:',revision,flush=True)
