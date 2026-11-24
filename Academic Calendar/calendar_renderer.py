"""Render local calendar files from the dated, sourced records in events.json."""
from pathlib import Path
from datetime import datetime,date,time,timedelta,timezone
import calendar,hashlib,html,json,re

ROOT=Path(__file__).resolve().parent
def esc(s):return html.escape(str(s),quote=True)
def text_ics(s):return str(s).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
def fold(s):
    parts=[];line='';size=0
    for c in s:
        n=len(c.encode('utf-8'))
        if size+n>75:parts.append(line);line=' '+c;size=1+n
        else:line+=c;size+=n
    return '\r\n'.join(parts+[line])
def when(e):
    d=datetime.fromisoformat(e['start']);s=d.strftime('%a %d %b')
    s+=' · '+d.strftime('%H:%M') if len(e['start'])>10 else ' · date only / see notes'
    if e.get('end'):
        if len(e['end'])>10:s+='–'+datetime.fromisoformat(e['end']).strftime('%H:%M')
        elif date.fromisoformat(e['end'])>d.date()+timedelta(days=1):s+=' (window through '+(date.fromisoformat(e['end'])-timedelta(days=1)).strftime('%d %b')+')'
    return s
def is_active(e,today):
    start=date.fromisoformat(e['start'][:10])
    if e.get('completed'):return False
    if start>=today:return True
    return bool(e.get('end') and date.fromisoformat(e['end'][:10])>today)

def write_ics(filename,title,events,data):
    asof=datetime.fromisoformat(data['as_of']);stamp=asof.strftime('%Y%m%dT%H%M%SZ')
    lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Study Calendar//UCL Term 1 Snapshot//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:'+text_ics(title),'X-WR-TIMEZONE:Europe/London']
    for e in events:
        uid=hashlib.sha256(e['id'].encode()).hexdigest()[:24]+'@ucl-study-calendar.local'
        lines+=['BEGIN:VEVENT','UID:'+uid,'DTSTAMP:'+stamp,'LAST-MODIFIED:'+stamp,'SEQUENCE:'+str(data.get('sequence',2)),'CLASS:PRIVATE']
        all_day=len(e['start'])==10
        if all_day:
            start=date.fromisoformat(e['start']);end=date.fromisoformat(e['end']) if e.get('end') else start+timedelta(days=1)
            lines+=['DTSTART;VALUE=DATE:'+start.strftime('%Y%m%d'),'DTEND;VALUE=DATE:'+end.strftime('%Y%m%d')]
        else:
            # All timed records in this snapshot fall in UK winter time (UTC).
            start=datetime.fromisoformat(e['start']).replace(tzinfo=timezone.utc)
            lines+=['DTSTART:'+start.strftime('%Y%m%dT%H%M%SZ')]
            if e.get('end'):lines+=['DTEND:'+datetime.fromisoformat(e['end']).strftime('%Y%m%dT%H%M%SZ')]
        description=e['notes']+'\n\nCertainty: '+e['certainty']+'\nUK time (Europe/London, GMT).\nSnapshot: '+asof.strftime('%d %B %Y')+'; not automatically updated.\nSources:\n'+'\n'.join(e['sources'])
        lines+=['SUMMARY:'+text_ics(e['title']),'DESCRIPTION:'+text_ics(description),'CATEGORIES:'+text_ics(e['category'].upper())+','+text_ics(e['course']),'URL:'+e['sources'][0],
                'STATUS:'+('CONFIRMED' if e['certainty']=='Published' else 'TENTATIVE'),'TRANSP:'+('OPAQUE' if e['category']=='Teaching' else 'TRANSPARENT')]
        if e['category']=='Assessment':
            if all_day:
                reminder=datetime.combine(start-timedelta(days=1),time(9),tzinfo=timezone.utc)
                if reminder>asof:lines+=['BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+text_ics(e['title']+' — confirm any unpublished time'),'TRIGGER;VALUE=DATE-TIME:'+reminder.strftime('%Y%m%dT%H%M%SZ'),'END:VALARM']
            else:
                for seconds,trigger in [(259200,'-P3D'),(86400,'-P1D'),(7200,'-PT2H')]:
                    if start-timedelta(seconds=seconds)>asof:lines+=['BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+text_ics(e['title']),'TRIGGER:'+trigger,'END:VALARM']
        lines+=['END:VEVENT']
    lines+=['END:VCALENDAR']
    (ROOT/filename).write_bytes(('\r\n'.join(fold(line) for line in lines)+'\r\n').encode('utf-8'))

def main():
    data=json.loads((ROOT/'events.json').read_text(encoding='utf-8'))
    today=date.fromisoformat(data['period_start']);last=date.fromisoformat(data['period_end']);asof=datetime.fromisoformat(data['as_of'])
    events=[e for e in data['events'] if is_active(e,today) and date.fromisoformat(e['start'][:10])<=last]
    core=[e for e in events if not e['optional']];optional=[e for e in events if e['optional']];assessments=[e for e in core if e['category']=='Assessment']
    week_end=date.fromisoformat(data['week_end']);week=[e for e in events if date.fromisoformat(e['start'][:10])<=week_end]
    write_ics('term1-calendar.ics','UCL Term 1 — remaining assessments and teaching',core,data)
    write_ics('assessments-only.ics','UCL Term 1 — remaining assessments',assessments,data)
    write_ics('published-assessments.ics','UCL Term 1 — assessments with published dates',[e for e in assessments if e.get('date_verified',True)],data)
    write_ics('optional-support.ics','UCL Term 1 — optional support and events',optional,data)

    md=['# UCL calendar for the remainder of Term 1','',f'Updated **{asof.strftime("%d %B %Y")}**, for **Team 21**, in **UK time / GMT**. This week is **23–29 November**, teaching Week 7 / UCL academic Week 13. Term ends 18 December; the required IPAC deadline on 23 December is also included.','',
        '**Haskell test: Thursday 17 December at 10:00, worth 5%.** The current introduction slides confirm the date. The earlier unconfirmed 14 December marker has been replaced. [Introduction slides, page 2](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9502411).','',
        '## Open or import','',
        '- [Visual calendar and agenda](term1-schedule.html)',
        '- [Main calendar](term1-calendar.ics)',
        '- [Assessments only](assessments-only.ics)',
        '- [Optional support and events](optional-support.ics)','',
        'Import either the main calendar or assessments-only; main already contains the assessments. Replace the earlier imported calendar rather than importing this snapshot alongside it to avoid duplicates. The Haskell event retains its UID and has moved to 17 December. No calendar account has been changed.','',
        '## Changes since 15 November','']
    for c in data['changes']:md.append('- **['+c['title']+']('+c['source']+')** — '+c['text'])
    md+=['','## Priorities for 23 to 29 November','']
    for i,c in enumerate(data['week_priorities'],1):md.append(str(i)+'. **['+c['title']+']('+c['source']+')** — '+c['text'])
    md+=['','## This week’s dated activities','', '| When | Item | Details |','| --- | --- | --- |']
    for e in week:md.append('| '+when(e)+' | ['+e['title']+']('+e['sources'][0]+') | '+e['notes']+' |')
    md+=['','## Remaining graded assessment dates','', 'Percentages are shares of the relevant module. Date-only entries do not imply a 23:59 cutoff.','', '| When | Assessment | Weight | Details |','| --- | --- | --- | --- |']
    for e in assessments:md.append('| '+when(e)+' | ['+e['title']+']('+e['sources'][0]+') | '+str(e['weight'])+' | '+e['notes']+' |')
    md+=['','## Teaching and optional support through term end','']
    for e in events:
        if e['category']=='Assessment':continue
        md.append('- **'+when(e)+'** — ['+e['title']+']('+e['sources'][0]+'). '+e['notes'])
    md+=['','## Project notices','']
    for c in data['project_notices']:md.append('- **['+c['title']+']('+c['source']+')** — '+c['text'])
    md+=['','## Completed work','']
    for c in data['completed_work']:md.append('- **['+c['title']+']('+c['source']+')** — '+c['status'])
    md+=['','## Details still to check','']
    for title,notes,url in data['watchlist']:md.append('- **['+title+']('+url+')** — '+notes)
    md+=['','## Source coverage','',data['limits'],'',
        'This is an update of the [15 November resource audit](audit-2026-11-15/audit-report.md). The current source responses and change records are in [the 23 November update folder](audit-2026-11-23/moodle-index.json). Recordings, hidden items and individual timetable changes may add information.','']
    reading='\n'.join(md);(ROOT/'term1-schedule.md').write_text(reading,encoding='utf-8')
    (ROOT/data['audit_report']).write_text(reading.replace('# UCL calendar for the remainder of Term 1','# Moodle calendar update for 23 November 2026',1).replace('](term1-','](../term1-').replace('](assessments-only.ics)','](../assessments-only.ics)').replace('](optional-support.ics)','](../optional-support.ics)').replace('](audit-2026-11-15/','](../audit-2026-11-15/').replace('](audit-2026-11-23/moodle-index.json)','](moodle-index.json)'),encoding='utf-8')

    cards=[]
    for e in events:
        links=' · '.join('<a href="'+esc(url)+'" target="_blank" rel="noopener">Source '+str(i+1)+'</a>' for i,url in enumerate(e['sources']))
        cards.append('<article class="event '+e['category'].lower()+'" data-optional="'+str(e['optional']).lower()+'" data-course="'+esc(e['course'])+'" data-kind="'+e['category']+'"><div class="date">'+esc(when(e))+'</div><div><div class="tag">'+esc(e['course']+' · '+e['category'])+'</div><h3>'+esc(e['title'])+'</h3><p>'+esc(e['notes'])+'</p><p class="certainty">'+esc(e['certainty'])+'</p><div class="links">'+links+'</div></div></article>')
    months=[]
    for month in [11,12]:
        cells=[]
        for cal_week in calendar.Calendar(firstweekday=0).monthdatescalendar(2026,month):
            for d in cal_week:
                if d.month!=month:cells.append('<div class="day muted"></div>');continue
                cell='<div class="day '+('outside' if not today<=d<=last else '')+'"><span class="dayno">'+str(d.day)+'</span>'
                for e in core:
                    if e['start'][:10]!=d.isoformat():continue
                    label=e['title'].replace('ENGF0034: ','').replace('ENGF0001: ','').replace('DUE: ','').replace('ASSESSMENT: ','')
                    prefix=e['start'][11:]+' ' if len(e['start'])>10 else ''
                    cell+='<a class="chip '+e['category'].lower()+'" href="#agenda" title="'+esc(e['title'])+'">'+esc(prefix+label)+'</a>'
                cells.append(cell+'</div>')
        months.append('<section class="month"><h2>'+calendar.month_name[month]+' 2026</h2><div class="grid weekdays">'+''.join('<div>'+d+'</div>' for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])+'</div><div class="grid">'+''.join(cells)+'</div></section>')
    changes=''.join('<li><a href="'+esc(c['source'])+'"><strong>'+esc(c['title'])+'</strong></a> — '+esc(c['text'])+'</li>' for c in data['changes'])
    priorities=''.join('<li><strong>'+esc(c['title'])+'</strong><p>'+esc(c['text'])+' <a href="'+esc(c['source'])+'">Source</a></p></li>' for c in data['week_priorities'])
    watch=''.join('<li><a href="'+esc(u)+'">'+esc(t)+'</a><p>'+esc(n)+'</p></li>' for t,n,u in data['watchlist'])
    project=''.join('<li><a href="'+esc(c['source'])+'">'+esc(c['title'])+'</a><p>'+esc(c['text'])+'</p></li>' for c in data['project_notices'])
    options=''.join('<option>'+esc(c)+'</option>' for c in sorted({e['course'] for e in events}))
    css=(ROOT/'calendar.css').read_text(encoding='utf-8')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>UCL calendar updated 23 November 2026</title><style>__CSS__</style><main>
<header><div class="eyebrow">UCL · Computer Science · Team 21</div><h1>Your UCL calendar<br>23 November to term end</h1><p>Updated 23 November 2026. UK time throughout. This week is 23–29 November, teaching Week 7 / UCL academic Week 13. Term ends 18 December, with IPAC still due on 23 December.</p><nav class="downloads"><a href="term1-calendar.ics" download>Main calendar</a><a href="assessments-only.ics" download>Assessments only</a><a href="optional-support.ics" download>Optional support</a><a href="term1-schedule.md">Full readable schedule</a></nav></header>
<div class="note"><strong>Haskell test date now confirmed: Thursday 17 December at 10:00 (5%).</strong> The new introduction slides replace the earlier unconfirmed 14 December marker. <a href="https://moodle.ucl.ac.uk/mod/resource/view.php?id=9502411">See page 2</a>. The C coursework is submitted.</div>
<div class="priorities"><div class="priority"><div class="label">This week’s graded deadline</div><h2>25 Nov · 23:59</h2><p>Tetris autoplayer · 20%<br>Push and verify receipt early.</p></div><div class="priority"><div class="label">Next report</div><h2>4 Dec · 14:00</h2><p>Individual Social Impact Report · 10%<br>Template, maximum 1,200 words + declaration.</p></div><div class="priority"><div class="label">New brief to watch for</div><h2>26 Nov · release</h2><p>CA5 Pacman specification · 15%<br>Due 10 Dec; exact cutoff still TBC.</p></div></div>
<h2>What changed</h2><div class="watch"><ul>__CHANGES__</ul></div><h2>Priorities for 23 to 29 November</h2><div class="watch"><ol>__PRIORITIES__</ol></div>
<p class="legend">Orange = graded assessment · Green = published teaching or milestone · Purple = preparation or release. Timetable-check windows mark a period in which a session occurs, not an all-day booking. Month grids show the main calendar; optional support is in the agenda filter.</p>__MONTHS__
<h2 id="agenda">Agenda and source notes</h2><p>Import main or assessments-only, not both. Replace your earlier imported calendar to avoid duplicates. Personal COMP0002/COMP0147 lecture, lab and PBL slots still require your timetable. The Week 7 Haskell page directs synchronous attendance through the Week 6 Zoom button.</p>
<div class="filters"><label>Show <select id="kind"><option value="main">Main calendar</option><option value="assessments">Assessments only</option><option value="optional">Optional support and events</option><option value="all">Everything</option></select></label><label>Course <select id="course"><option value="all">All courses</option>__OPTIONS__</select></label><button onclick="window.print()">Print / save PDF</button><span class="count" id="count" aria-live="polite"></span></div><div id="events">__CARDS__</div>
<h2>Project notices</h2><div class="watch"><ul>__PROJECT__</ul></div><h2>Details still to check</h2><div class="watch"><ul>__WATCH__</ul></div>
<footer><p>__LIMITS__</p><p><a href="audit-2026-11-23/update-report.md">23 November update and weekly plan</a> · <a href="events.json">Structured events</a> · <a href="audit-2026-11-15/audit-report.md">Previous full audit</a></p><p>This is a local snapshot and does not update automatically. No calendar account has been changed.</p></footer></main>
<script>const kind=document.getElementById('kind'),course=document.getElementById('course');function filter(){let n=0;document.querySelectorAll('.event').forEach(e=>{const m=kind.value,o=e.dataset.optional==='true';const v=(m==='all'||m==='main'&&!o||m==='optional'&&o||m==='assessments'&&e.dataset.kind==='Assessment')&&(course.value==='all'||course.value===e.dataset.course);e.hidden=!v;if(v)n++});document.getElementById('count').textContent=n+' entries'}kind.addEventListener('change',filter);course.addEventListener('change',filter);filter();</script></html>'''
    for key,value in {'CSS':css,'CHANGES':changes,'PRIORITIES':priorities,'MONTHS':''.join(months),'OPTIONS':options,'CARDS':''.join(cards),'PROJECT':project,'WATCH':watch,'LIMITS':esc(data['limits'])}.items():page=page.replace('__'+key+'__',value)
    (ROOT/'term1-schedule.html').write_text(page,encoding='utf-8')
    result={'as_of':data['as_of'],'core_events':len(core),'remaining_assessments':len(assessments),'optional_events':len(optional),'this_week_entries':len(week)}
    (ROOT/'audit-2026-11-23/build-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
