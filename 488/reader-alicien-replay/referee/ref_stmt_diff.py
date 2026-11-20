# Token diff: FC erdos_488 body vs Challenge.lean not_erdos_488 (inside ¬(...)) and erdos_488_card_le_two.
import re,sys
D='/home/exedev/MathDyad/erdos488/alicien/'
fc=open(D+'fc_488_main.lean').read(); ch=open(D+'src/repo/Challenge.lean').read(); st=open(D+'src/repo/Erdos488/Statement.lean').read()
def strip_comments(s): return re.sub(r'--[^\n]*','',s)
def body(s,start,end):
    i=s.index(start)+len(start); j=s.index(end,i); return s[i:j]
tok=lambda s: re.findall(r'[A-Za-z_][\w.]*|\d+|∀ᵉ|[^\s\w]',strip_comments(s))
f=tok(body(fc,'theorem erdos_488 :',':= by'))
c1=tok(body(ch,'theorem Erdos488.not_erdos_488 :',':= by'))
c2=tok(body(ch,'theorem Erdos488.erdos_488_card_le_two :',':= by'))
s=tok(body(st,'def Erdos488Prop : Prop :=','\n\nend'))
print('FC tokens',len(f)); 
print('Challenge#1 == ¬ ( FC ) :', c1==['¬','(']+f+[')'])
print('Statement.lean Erdos488Prop == FC :', s==f)
# card_le_two: FC with "A.card ≤ 2 →" inserted after "A.Nonempty →"
k=f.index('→')+1
print('Challenge#2 == FC with A.card ≤ 2 → inserted :', c2==f[:k]+['A.card','≤','2','→']+f[k:])
