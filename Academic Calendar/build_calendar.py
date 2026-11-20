"""Build a sourced calendar snapshot. Run with Python 3.11; no runtime dependencies."""
from pathlib import Path
from datetime import datetime, date, time, timedelta, timezone
import calendar
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parent
STAMP = '20261115T155413Z'
ASOF = datetime(2026, 11, 15, 15, 54, 13, tzinfo=timezone.utc)
MOODLE = 'https://moodle.ucl.ac.uk/'
def section(n): return MOODLE + f'course/section.php?id={n}'
def module(kind, n): return MOODLE + f'mod/{kind}/view.php?id={n}'
EVENTS = []
def add(key, title, start, category, course, notes, source, end=None, optional=False, certainty='Published', weight=None):
    EVENTS.append(dict(id=key, title=title, start=start, end=end, category=category,
                       course=course, notes=notes, sources=source if isinstance(source, list) else [source],
                       optional=optional, certainty=certainty, weight=weight))

add('comp0002-c', 'DUE: COMP0002 C maze coursework (5%)', '2026-11-18T16:00', 'Assessment', 'COMP0002',
    'Submit COMP0002CW1.zip to Moodle: C source, readMe (maximum one page), and required data/images. Exclude compiled files and the supplied DrawApp files. Brief and Moodle agree on 16:00 UK time. Moodle status rechecked on 15 November: new, not submitted. Personal extensions may change your deadline.',
    [module('assign',8508448), module('resource',8508574)], weight='5%')
add('engf0034-ca4', 'DUE: ENGF0034 CA4 Tetris autoplayer (20%)', '2026-11-25T23:59', 'Assessment', 'ENGF0034',
    'Deadline date from the current course calendar; exact 23:59 UK time from the linked assignment brief. Set up UCL GitLab, sign in to the grading server, enrol in Tetris and push code to your fork. Check the server has received and run your submitted version. Moodle assignment status does not cover this external submission.',
    [section(1467895), 'https://github.com/UCL-ENGF0034-2026/course-materials/blob/main/Assignment%204%20brief/assignment4.pdf'], weight='20%')
add('engf0001-social', 'DUE: ENGF0001 Individual Social Impact Report (10%)', '2026-12-04T14:00', 'Assessment', 'ENGF0001',
    'Individual submission using the supplied template, Word or PDF, maximum 1,200 words. Complete the referencing / generative AI declaration form as part of submission. Current submission instructions give the word limit; older overview text calls this a two-page report. Moodle status rechecked on 15 November: new (not submitted), last modified 13 November at 20:09.',
    [module('assign',9105891), section(1467589), module('url',9105890)], weight='10%')
add('engf0034-ca5', 'DUE: ENGF0034 CA5 Pacman specification (15%) — TIME TBC', '2026-12-10', 'Assessment', 'ENGF0034',
    'The 2026 course calendar places CA5 due on Thursday 10 December. No cutoff time, submission link or CA5 brief was published in the accessible material. This is a date-only deadline, not a 23:59 deadline. Check the brief when released on 26 November. Weight and task name are from How to use this course.',
    [section(1467895), section(1467896)], certainty='Date published; time and submission route TBC', weight='15%')
add('engf0001-demo', 'ASSESSMENT: ENGF0001 Team 21 bioreactor demo (10%) — TIME TBC', '2026-12-14', 'Assessment', 'ENGF0001',
    'The current Task 10.1 page explicitly says Monday 14 December 2026. The 2026 timetable places demonstrations in MPEB 6.02 during the afternoon. The downloadable DemoSchedule.pdf is explicitly dated 8 December 2025: its Team 21 slot of 16:00–16:40 is historical and is NOT a confirmed 2026 booking. Obtain the updated Team 21 slot before attending. The instructions describe a live working-system demo and viva; all team members should be ready to explain the system.',
    [module('page',9105595),module('resource',9105507),module('resource',9105597)], certainty='Date published; Team 21 time TBC', weight='10%')
add('engf0001-final', 'DUE: ENGF0001 Team Final Report (30%)', '2026-12-18T14:00', 'Assessment', 'ENGF0001',
    'One team member submits a Word or PDF report; one member also completes the referencing and AI tools declaration. Use the supplied report template and rubric. The overview says 9 pages excluding references/appendices, while the submission box describes a penalty above 10 pages excluding references: target the stricter 9-page guidance and clarify the limit. Moodle status rechecked on 15 November: not submitted.',
    [module('assign',9105625),section(1467573),module('url',9105624)], weight='30%')
add('engf0001-ipac', 'DUE: ENGF0001 Individual Contribution to Teamwork / IPAC (10%)', '2026-12-23T14:00', 'Assessment', 'ENGF0001',
    'AFTER TERM ENDS: included because it is a required assessment arising from this term. Personally complete the IPAC ratings and feedback for your teammates and yourself. The explicit assessment deadline is 14:00 on 23 December; a later closing date inside IPAC allows late submission and does not replace this deadline. Weekly minutes are part of this component: the team should submit at least six records, aiming for within 48 hours of each on-campus team meeting.',
    [section(1467573),module('lti',9105609),module('url',9105606)], weight='10%')

add('comp0002-haskell-provisional', 'UNCONFIRMED: COMP0002 Haskell test (5%) — classmate-reported date', '2026-12-14', 'Assessment', 'COMP0002',
    'DATE NOT VERIFIED: a classmate reportedly recalled 14 December from an early lecture. The test itself and 5% weighting are confirmed by Slides 1, page 8. All accessible programming PDFs, current sections and standard forum announcements were rechecked on 15 November; none establishes this date. Spoken announcements and Panopto transcripts were not accessible, so the classmate may still be correct. This all-day tentative marker is a planning precaution, not a confirmed test booking. Time, venue and date must be confirmed with Dr David Clark or in the personal timetable. It falls on the confirmed ENGF0001 demo date, so check for a potential clash; no clash is established without the times.',
    [module('resource',8508469), module('resource',8508455), section(1378607)], certainty='UNCONFIRMED date: classmate report only; test and 5% weight confirmed', weight='5%')
add('haskell-start', 'COMP0002: Haskell teaching starts this week', '2026-11-16', 'Milestone', 'COMP0002',
    'The functional programming half runs 16 November–18 December. The first module slides confirm a 5% Haskell in-class test and a 90% Term 3 exam. A classmate reports 14 December for the test, but no written confirmation was found. Confirm the test date/time with Dr David Clark; consult your personal timetable for lectures and your allocated lab.',[section(1378607),module('resource',8508469)])
add('ethics-tasks', 'ENGF0034: Ethics tasks this week', '2026-11-23', 'Preparation', 'ENGF0034',
    'The course calendar lists Ethics tasks on Monday of this week, before Tuesday’s ethics lecture. Review the ethics videos, case studies, canvas and reflection activity. No separate submission deadline was found; this entry is preparation, not a graded deadline.',[section(1467895),section(1467898)])
add('ca5-release', 'RELEASE: ENGF0034 CA5 and Pacman video', '2026-11-26', 'Release', 'ENGF0034',
    'The course calendar schedules the CA5 release and CA5.0 Pacman video today. Read the new brief to confirm the exact 10 December cutoff and submission method.',section(1467895))
add('term-end', 'Term 1 ends', '2026-12-18', 'Milestone', 'Programme',
    'Programme term dates confirm 18 December as the end of Term 1. IPAC is still due on 23 December.',section(1484798))

# Repeat only dates explicitly covered by the 2026 course calendar/timetable.
for d in ['2026-11-17','2026-11-24','2026-12-01','2026-12-08','2026-12-15']:
    ethics = d == '2026-11-24'
    add('dps-tue-'+d, 'ENGF0034: '+('Ethics lecture / activity' if ethics else 'CS lecture'), d+'T11:00', 'Teaching', 'ENGF0034',
        'Birkbeck Euston Road (373), room 402. Start time published as 11:00; end time is not published in the Moodle calendar. Check your personal timetable for the duration and any changes.',section(1467895))
for d in ['2026-11-20','2026-11-27','2026-12-04','2026-12-11']:
    add('dps-fri-'+d, 'ENGF0034: CS tutorial', d+'T11:00', 'Teaching', 'ENGF0034',
        'Medical Sciences 131, A V Hill Lecture Theatre. Start time published as 11:00; end time is not published. The calendar does not list an 11:00 tutorial on 18 December, so none has been invented.',section(1467895))
for monday in [date(2026,11,16),date(2026,11,23),date(2026,11,30),date(2026,12,7)]:
    for offset, start, end in [(0,'16:00','18:00'),(2,'11:00','13:00')]:
        d=(monday+timedelta(days=offset)).isoformat()
        add('challenges-'+d, 'ENGF0001: Team 21 timetabled session (C/D)', d+'T'+start, 'Teaching', 'ENGF0001',
            'Team 21 falls in cohort C (teams 18–25), based on the module announcement. The updated 2026 timetable places C/D on Mondays 16:00–18:00 and Wednesdays 11:00–13:00 during project weeks 6–9. It lists parallel rooms MPEB 6.02 and Roberts 704 without resolving your room: confirm your allocation in the personal timetable. Session purpose may include project work or another timetabled activity. Agree who will submit the team meeting minutes and aim to do so within 48 hours after the meeting.',
            [module('resource',9105507),module('forum',9105151),module('url',9105606)], end=d+'T'+end, certainty='Published cohort times; room allocation TBC')
add('challenges-dec16', 'ENGF0001: Team 21 timetabled session (cohort C)', '2026-12-16T11:00', 'Teaching', 'ENGF0001',
    'The updated 2026 timetable lists cohort C on Wednesday of project week 10 at 11:00–13:00 in Maths 505, Gordon Street (25). Check the personal timetable and announcements for the purpose/venue before attending. This is separate from the demo on 14 December.',
    module('resource',9105507), end='2026-12-16T13:00', certainty='Published timetable; recheck venue/purpose')

# Optional support and engagement items are kept in their own import file.
for monday in [date(2026,11,16)+timedelta(weeks=i) for i in range(5)]:
    for offset,start,end in [(2,'15:00','16:00'),(3,'16:00','17:00'),(4,'13:00','14:00')]:
        d=(monday+timedelta(days=offset)).isoformat()
        add('clinic-'+d, 'OPTIONAL: ENGF0034 CS drop-in clinic', d+'T'+start, 'Support', 'ENGF0034',
            'Henry Morley building, G03 (the course calendar prints GO3). No booking required; bring questions or come if you are unsure where to start.',section(1467895),end=d+'T'+end,optional=True)
    d=(monday+timedelta(days=4)).isoformat()
    add('admin-'+d, 'OPTIONAL: Undergraduate teaching/admin drop-in', d+'T09:00', 'Support', 'Student Hub',
        'MS Teams, no appointment. Useful for timetable, module and study-support queries. Open the Moodle section for the join link.',section(1463351),end=d+'T10:00',optional=True)
for d,start,end in [('2026-11-17','14:00','15:00'),('2026-12-01','14:00','15:00'),('2026-12-15','13:00','14:00')]:
    add('office-'+d, 'OPTIONAL: ENGF0034 office hour', d+'T'+start, 'Support', 'ENGF0034',
        '169 Euston Road, room 208. Times from the dated course calendar.',section(1467895),end=d+'T'+end,optional=True)
add('acc-window','OPTIONAL WINDOW: ACC one-to-one tutorials','2026-11-16','Support','ACC',
    'Booking window, not an appointment: Round 1 runs 16 November–18 December. Book a 30-minute MS Teams tutorial on writing, presentations or learning strategies. A booked slot must be added separately.',module('scheduler',8605107),end='2026-12-19',optional=True)
add('pulse-target','COMP0002 pulse survey: requested completion','2026-11-18T10:00','Survey','COMP0002',
    'Moodle calendar target completion time. This is a feedback survey, not coursework. The actual closing time is 20 November at 23:59.',module('feedback',8582586),optional=True)
for course,mid in [('COMP0002',8582586),('COMP0147',8625370)]:
    add('pulse-close-'+course, course+' pulse survey closes','2026-11-20T23:59','Survey',course,
        'Feedback survey closing time from Moodle calendar; not a graded assessment.',module('feedback',mid),optional=True)
add('mentor-nominations','OPTIONAL: Transition Mentor award nominations close — TIME TBC','2026-11-20','Event','Transition',
    'The Moodle link says nominations close 20 November; no cutoff time is supplied. Optional nomination, not an assessment.',module('url',9500064),optional=True,certainty='Date published; time TBC')
add('mentor-final','WINDOW: Final Transition Mentor session — TIME TBC','2026-11-23','Event','Transition',
    'The final wrap-up session is in the week commencing 23 November. The week-long entry marks a scheduling window, not a meeting every day. Confirm your actual session with your mentor. Programme evaluation survey also mentioned, with no fixed deadline.',section(1434967),end='2026-11-28',optional=True,certainty='Week published; personal meeting TBC')
add('mentor-awards','OPTIONAL: Transition Mentor Awards Evening — TIME TBC','2026-12-10','Event','Transition',
    'The Moodle booking link names 10 December. Time/venue and registration must be checked using the booking page; no attendance assumed.',module('url',9500068),optional=True,certainty='Date published; time/venue TBC')
add('careers-focus','OPTIONAL: Engineering teamwork focus group — SLOT TBC','2026-11-19','Event','Careers',
    'The 5 November Careers announcement advertises Thursday 19 November, UCL Bloomsbury, around one hour, with 17:00 or 18:00 slots. The MCP returns only an excerpt, so a full slot and registration details are unverified. Read the full announcement before booking; this all-day marker is not a confirmed reservation.',module('forum',8764831),optional=True,certainty='Announcement excerpt; registration/slot TBC')
for course,mid in [('COMP0002',8582588),('COMP0147',8625372)]:
    add('evaluation-window-'+course, 'OPTIONAL: '+course+' module evaluation window starts', '2026-12-14', 'Survey', course,
        'The current survey section lists the evaluation window as 14 December 2026–22 January 2027. This marker denotes the window opening, not an assessment or a meeting. No exact closing time is supplied; the closing date is beyond this Term 1 calendar.',
        module('questionnaire',mid), optional=True)

EVENTS.sort(key=lambda e:(e['start'],e['title']))

WATCHLIST = [
    ('COMP0002 Haskell in-class test: 14 December is unconfirmed', 'Slides 1, page 8 confirms the test is worth 5%; the classmate reports 14 December from an early lecture. No accessible written source gives that date. The calendar includes a tentative all-day marker labelled UNCONFIRMED, not a booked test. Confirm date, time and venue with Dr David Clark at the first Haskell session; 14 December is also the confirmed Engineering Challenges demo date.', module('resource',8508469)),
    ('COMP0147 exam: 100% of the module; mock date TBC', 'The official 2026/27 UCL catalogue confirms 100% Exam. No exact exam date/time or duration was found. Week 10 mentions a mock test with no date or graded weighting. The exercise sheets are practice, and exam-style questions in them are not new deadlines. No exam booking has been invented.', 'https://www.ucl.ac.uk/module-catalogue/modules/discrete-mathematics-for-computer-scientists-COMP0147'),
    ('COMP0147 weekly lectures and PBL', 'Attend your allocated lecture/PBL sessions and work through the problem lists. The November announcement says teaching resumes on Tuesday 17 November; October posts mention a 09:00 main lecture and afternoon PBL, but they do not establish the remaining term timetable. No recurring times have been inferred from those posts.', module('forum',8511614)),
    ('COMP0002 lectures and allocated programming lab', 'The module specifies three lecture hours and one two-hour allocated lab per teaching week; group times require the personal timetable. These sessions are not in the generated calendar.', section(1378607)),
    ('ENGF0001 Team 21 demo time', '14 December 2026 is confirmed by Task 10.1. The attached demo schedule is dated 8 December 2025 and gives Team 21 a historical 16:00–16:40 slot. Do not use that slot as a 2026 booking; request the current schedule.', module('resource',9105597)),
    ('ENGF0001 social-impact workshop', 'The social-impact page says the workshop is in a Monday afternoon or Wednesday morning slot and to check the personal timetable. The 25 November reference concerns release of slides/recording, not a confirmed personal workshop booking.', section(1467589)),
    ('ENGF0001 report-writing sessions', 'The Week 7 page mentions 5 and 7 December, with no times. 5 December 2026 is a Saturday, and the surrounding teaching material includes old dates. These two dates are listed for confirmation and have not been imported as confirmed sessions.', section(1467569)),
    ('CA5 exact submission time and route', '10 December is the date in the current course calendar. The linked GitHub repository has no CA5 brief at this snapshot. Check the scheduled 26 November release; no 23:59 cutoff has been invented.', section(1467895)),
    ('ENGF0034 ethics report is in Term 2', 'The 2026 opening lecture places the ethics report (15%) in Term 2, week 7; presentations (10%) in Term 2 Reading Week; scenarios (40%) in Term 2. They have no verified current exact submission dates here and are outside this Term 1 calendar. The 23 November ethics tasks and 24 November lecture remain current teaching activities. Ignore the stale February 2021 date.', 'https://github.com/UCL-ENGF0034-2026/course-materials/blob/main/Week%201/ENGF34-2026%20Opening%20lecture.pdf'),
    ('Personal extensions and timetable changes', 'The calendar is based on visible course-level dates, not an independently verified extension record or your personal timetable. Check the Moodle submission box for any extension and UCL Timetable for group/room changes.', module('url',9207933)),
]

HISTORY = [
    ('ENGF0034 CA1', '12 Oct 2026, 11:00', 'Submitted', module('assign',9108695)),
    ('ENGF0034 CA2 Bomber', '20 Oct 2026, 11:00 in assignment API', 'Submitted; descriptive text/announcement says midday, so times conflict', module('assign',9108700)),
    ('ENGF0034 CA3 Frogger', '2 Nov 2026, 23:59', 'Submitted', module('assign',9108708)),
    ('ENGF0001 proposal slides', '3 Nov 2026, 09:00', 'Submitted; staff announcement resolves stray 16 November text to 3 November', module('assign',9105614)),
    ('ENGF0001 IPAC criteria', '6 Nov 2026, 14:00', 'Submitted; API last-modified time is 18:41 that day, which alone does not establish whether any penalty applies', module('assign',9105605)),
    ('ENGF0001 Challenge 1 video / peer assessment', '23 Oct / 30 Oct 2026, 14:00 (late-video peer assessment: 6 Nov)', 'Completion unverified: workshop status is not exposed by the available tool. Check both phases in Moodle.', module('workshop',9105469)),
    ('Compulsory induction / Active Bystander', 'Earlier in term; personal workshop slot', 'Completion unverified. Check the online module and workshop attendance if unsure.', section(1463347)),
]

def escape_ics(value):
    return str(value).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
def folded(line):
    result=[]; part=''; used=0
    for ch in line:
        n=len(ch.encode('utf-8'))
        if used+n>75:
            result.append(part); part=' '+ch; used=1+n
        else:
            part+=ch; used+=n
    result.append(part)
    return '\r\n'.join(result)
def ics_event(e):
    uid=hashlib.sha256(e['id'].encode()).hexdigest()[:24]+'@ucl-study-calendar.local'
    lines=['BEGIN:VEVENT','UID:'+uid,'DTSTAMP:'+STAMP,'LAST-MODIFIED:'+STAMP,'SEQUENCE:1','CLASS:PRIVATE']
    all_day=len(e['start'])==10
    if all_day:
        start=date.fromisoformat(e['start'])
        end=date.fromisoformat(e['end']) if e['end'] else start+timedelta(days=1)
        lines+=['DTSTART;VALUE=DATE:'+start.strftime('%Y%m%d'),'DTEND;VALUE=DATE:'+end.strftime('%Y%m%d')]
    else:
        start=datetime.fromisoformat(e['start']).replace(tzinfo=timezone.utc)
        lines+=['DTSTART:'+start.strftime('%Y%m%dT%H%M%SZ')]
        if e['end']:
            end=datetime.fromisoformat(e['end']).replace(tzinfo=timezone.utc)
            lines+=['DTEND:'+end.strftime('%Y%m%dT%H%M%SZ')]
    description=(e['notes']+'\n\nCertainty: '+e['certainty']+'\nTimezone: Europe/London (GMT during this calendar).\nSnapshot: 15 November 2026; this file does not sync automatically.\nSources:\n'+'\n'.join(e['sources']))
    lines+=['SUMMARY:'+escape_ics(e['title']),'DESCRIPTION:'+escape_ics(description),'CATEGORIES:'+e['category'].upper()+','+escape_ics(e['course']), 'URL:'+e['sources'][0], 'STATUS:'+('TENTATIVE' if e['certainty']!='Published' else 'CONFIRMED'),'TRANSP:'+('OPAQUE' if e['category']=='Teaching' else 'TRANSPARENT')]
    if e['category']=='Assessment':
        # Reminder times are planning aids, never claimed submission cutoffs.
        if not all_day:
            for seconds,trigger in [(259200,'-P3D'),(86400,'-P1D'),(7200,'-PT2H')]:
                if start-timedelta(seconds=seconds)>ASOF:
                    lines+=['BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+escape_ics(e['title']),'TRIGGER:'+trigger,'END:VALARM']
        else:
            reminder=datetime.combine(date.fromisoformat(e['start'])-timedelta(days=1),time(9),tzinfo=timezone.utc)
            lines+=['BEGIN:VALARM','ACTION:DISPLAY','DESCRIPTION:'+escape_ics(e['title']+' — confirm the time'),'TRIGGER;VALUE=DATE-TIME:'+reminder.strftime('%Y%m%dT%H%M%SZ'),'END:VALARM']
    return lines+['END:VEVENT']
def write_ics(filename,name,events):
    lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Study Calendar//UCL Term 1 2026 Snapshot//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:'+escape_ics(name),'X-WR-TIMEZONE:Europe/London']
    for e in events: lines.extend(ics_event(e))
    lines+=['END:VCALENDAR']
    (ROOT/filename).write_bytes(('\r\n'.join(folded(line) for line in lines)+'\r\n').encode('utf-8'))

CORE=[e for e in EVENTS if not e['optional']]
OPTIONAL=[e for e in EVENTS if e['optional']]
ASSESSMENTS=[e for e in EVENTS if e['category']=='Assessment']
write_ics('term1-calendar.ics','UCL Term 1 — assessments and published teaching',CORE)
write_ics('assessments-only.ics','UCL Term 1 — assessments only',ASSESSMENTS)
write_ics('published-assessments.ics','UCL Term 1 — assessments with published dates',[e for e in ASSESSMENTS if e['id']!='comp0002-haskell-provisional'])
write_ics('optional-support.ics','UCL Term 1 — optional support and events',OPTIONAL)
(ROOT/'events.json').write_text(json.dumps(dict(as_of=ASOF.isoformat(),timezone='Europe/London',term_end='2026-12-18',team=21,events=EVENTS,watchlist=WATCHLIST),indent=2,ensure_ascii=False),encoding='utf-8')

def when(e):
    dt=datetime.fromisoformat(e['start'])
    result=dt.strftime('%a %d %b')
    result+=' · '+dt.strftime('%H:%M') if len(e['start'])>10 else ' · date only / see notes'
    if e['end'] and len(e['end'])>10: result+='–'+datetime.fromisoformat(e['end']).strftime('%H:%M')
    if e['end'] and len(e['end'])==10: result+=' (window through '+(date.fromisoformat(e['end'])-timedelta(days=1)).strftime('%d %b')+')'
    return result

md=['# Your UCL calendar: remainder of Term 1, 2026/27','',
    'Updated **15 November 2026**, for **Team 21**, in **Europe/London (GMT)**. Term ends **18 December**; the required **23 December IPAC deadline** is included as an explicit exception. This is a snapshot, not a live subscription.','',
    '**Haskell test: a 5% assessment is confirmed, but 14 December is only a classmate-reported date.** It appears in the calendar as an explicitly UNCONFIRMED tentative marker. No accessible written source verified the date; recordings were not transcribed. [Full re-audit and coverage](audit-2026-11-15/audit-report.md).','',
    '## Open or import','',
    '- [Visual calendar and weekly agenda](term1-schedule.html)',
    '- [Main calendar: assessments, milestones and published teaching](term1-calendar.ics)',
    '- [Assessments only](assessments-only.ics)',
    '- [Optional clinics, office hours, surveys and events](optional-support.ics)','',
    '**Import either the main calendar or assessments-only, not both:** the main file already includes those assessments. Optional support is separate and can be added to either. Import into a new calendar in Google Calendar, Outlook or Apple Calendar. Re-importing snapshots may create duplicates. Alerts are included for assessments; your calendar app controls whether it honours them. No account calendar has been changed.','',
    'Timed entries use UK time. Date-only entries do not imply an end-of-day cutoff. Sessions with only a start time have no invented end time. TBC entries are marked tentative.','',
    '## Start here','',
    '1. **Prioritise the C coursework:** due Wednesday **18 November, 16:00**. Moodle currently reports `new`, not submitted. Package and verify the final zip before the cutoff.',
    '2. **Set up and start Tetris now:** due **25 November, 23:59** through GitLab / the grading server, not a Moodle upload. Allow time to see that the server received your code.',
    '3. **Plan the Social Impact Report:** due **4 December, 14:00**, using the current template and a maximum of 1,200 words. Include the declaration form.',
    '4. **Agree Team 21 roles and internal dates:** build/testing, demo rehearsal, report sections, final editor and minutes submission. These are planning decisions for your team; no internal deadlines have been invented as official dates.',
    '5. **Confirm the Haskell test date with Dr David Clark tomorrow, 16 November.** The reported 14 December date could coincide with the Engineering Challenges demo. The first lecture confirms its 5% weighting; the date is still unverified. Discrete Maths is 100% exam-assessed, with the exam/mock date unconfirmed. Check both phases of the earlier Challenge 1 video workshop if you are unsure they were completed.','',
    '## Assessment deadlines and demonstrations','',
    '| When (UK time) | Assessment | Weight | What to do |', '| --- | --- | --- | --- |']
for e in ASSESSMENTS:
    md.append('| '+when(e)+' | ['+e['title']+']('+e['sources'][0]+') | '+str(e['weight'])+' | '+e['notes']+' |')
md+=['','## Week-by-week schedule','',
    'The items below include the dated teaching sessions available in Moodle. COMP0002 lecture/lab slots and COMP0147 lecture/PBL slots still need to be added from your personal timetable.','']
for monday in [date(2026,11,9)+timedelta(weeks=i) for i in range(7)]:
    rows=[e for e in CORE if monday<=date.fromisoformat(e['start'][:10])<monday+timedelta(days=7)]
    if not rows: continue
    md+=['### Week of '+monday.strftime('%d %B'),'']
    for e in rows: md+=['- **'+when(e)+'** — ['+e['title']+']('+e['sources'][0]+'). '+e['notes']]
    md+=['']
md+=['## Optional support, surveys and events','', '| When | Item | Details |','| --- | --- | --- |']
for e in OPTIONAL: md.append('| '+when(e)+' | ['+e['title']+']('+e['sources'][0]+') | '+e['notes']+' |')
md+=['','## Dates or details to confirm','']
for title,notes,url in WATCHLIST: md+=['- **['+title+']('+url+')** — '+notes]
md+=['','## Earlier work: submitted versus unverified','',
    'These are historical checks, not new deadlines in the import files. A submission status alone does not establish a mark, punctuality or penalty.','',
    '| Item | Original date | Status as checked on 13 November |','| --- | --- | --- |']
for title,deadline,status,url in HISTORY: md.append('| ['+title+']('+url+') | '+deadline+' | '+status+' |')
md+=['','## What was checked and the limits','',
    '- Reviewed all 14 enrolled course outlines, and assignment/quiz listings and available forum discussions for the 13 current/support courses. The separately enrolled Engineering Challenges 25/26 course is historical and was excluded from the current calendar.',
    '- Read 44 targeted full sections, the current programme dates, weekly course calendars, assessment instructions, relevant page activities, the updated Challenge 2 timetable, demo schedule/instructions, C coursework brief, Tetris brief and team schedule workbook. The workbook is a blank planning template, not a list of booked team appointments.',
    '- The native calendar feed contained only the C coursework, two Engineering Challenges reports and survey dates. The text-based course calendar supplied the Tetris/Pacman dates; the assessment instructions supplied IPAC. No quizzes were listed in the 13 current/support courses. This does not exclude in-person tests or later releases.',
    '- COMP0005 Algorithms is labelled Term 2. No remainder-of-Term-1 assessment date was found. TechComm is a resource hub referring students back to the home module for assignments. No additional fixed current assessment date was found in ACC, IEP Central, programme/student hubs, TSG, mentoring or careers pages.',
    '- General optional ACC activities link to a separate central support course; no booking or personal appointment has been assumed. myUCLCareers and personal tutor/mentor appointments are not a complete external events feed.',
    '- Notifications failed twice with Moodle `invalidparameter`. The IPAC Moodle Book chapter text was blocked by Cloudflare; the current assessment section itself provided the IPAC deadline. Forum tools expose recent discussion excerpts rather than all full posts; the ENGF0034 student discussion activity is an `hsuforum` not listed by the standard forum tool. New or hidden announcements may add dates.',
    '- Old/copied dates were not rolled forward: ENGF0034 Scenario 1/2 assignments explicitly labelled 25/26, an August 2025 LSA deadline, the February 2021 ethics deadline, 2025 Miro text and the demo PDF dated December 2025 are not current deadlines. The staff announcement resolves the proposal-slide discrepancy to 3 November 2026.',
    '- Current report instructions supersede generic overview shorthand: the individual report is capped at 1,200 words. The team report has inconsistent 9/10-page guidance, noted above for clarification.',
    '- Personal extensions, COMP0002/COMP0147 class groups, room changes, external GitLab submission state, mentor appointment time and workshop completion are not independently verified. Check the linked source and your personal timetable before relying on a time.',
    '- [Source snapshot](sources/moodle-snapshot-2026-11-13.json) retains the Moodle responses used. [Structured event data](events.json) retains every event, uncertainty and source URL. No marks or feedback have been retrieved.','',
    'Review this calendar weekly and after new announcements. In particular, check the 26 November CA5 release and ask for the updated Team 21 demonstration timetable.','']
(ROOT/'term1-schedule.md').write_text('\n'.join(md),encoding='utf-8')

# Offline, printable reading view. All data and styles are embedded.
def esc(s): return html.escape(str(s),quote=True)
cards=[]
for e in EVENTS:
    links=' · '.join('<a href="'+esc(url)+'" target="_blank" rel="noopener">Source '+str(i+1)+'</a>' for i,url in enumerate(e['sources']))
    cards.append('<article class="event '+e['category'].lower()+'" data-optional="'+str(e['optional']).lower()+'" data-course="'+esc(e['course'])+'" data-kind="'+e['category']+'" data-date="'+e['start'][:10]+'"><div class="date">'+esc(when(e))+'</div><div><div class="tag">'+esc(e['course']+' · '+e['category'])+'</div><h3>'+esc(e['title'])+'</h3><p>'+esc(e['notes'])+'</p><p class="certainty">'+esc(e['certainty'])+'</p><div class="links">'+links+'</div></div></article>')
months=[]
for month in [11,12]:
    cells=[]
    for week in calendar.Calendar(firstweekday=0).monthdatescalendar(2026,month):
        for day in week:
            if day.month!=month: cells.append('<div class="day muted"></div>'); continue
            items=[e for e in CORE if e['start'][:10]==day.isoformat()]
            inside=date(2026,11,13)<=day<=date(2026,12,23)
            cell='<div class="day '+('outside' if not inside else '')+'"><span class="dayno">'+str(day.day)+'</span>'
            for e in items:
                label=e['title'].replace('ENGF0034: ','').replace('ENGF0001: ','').replace('DUE: ','').replace('ASSESSMENT: ','')
                prefix=e['start'][11:]+' ' if len(e['start'])>10 else ''
                cell+='<a class="chip '+e['category'].lower()+'" href="#agenda" title="'+esc(e['title'])+'">'+esc(prefix+label)+'</a>'
            cells.append(cell+'</div>')
    months.append('<section class="month"><h2>'+calendar.month_name[month]+' 2026</h2><div class="grid weekdays">'+''.join('<div>'+d+'</div>' for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])+'</div><div class="grid">'+''.join(cells)+'</div></section>')
watch=''.join('<li><a href="'+esc(url)+'">'+esc(title)+'</a><p>'+esc(notes)+'</p></li>' for title,notes,url in WATCHLIST)
course_options=''.join('<option>'+esc(c)+'</option>' for c in sorted({e['course'] for e in EVENTS}))
payload='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Your UCL term calendar · November–December 2026</title>
<style>
:root{color-scheme:light;--ink:#162b35;--soft:#53636c;--paper:#f3f5f2;--line:#d8e1db;--accent:#1c624e}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1280px;margin:auto;padding:40px 28px 70px}header{padding:36px;border-radius:20px;background:#153d36;color:white}.eyebrow{font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:#bce3cf}h1{font-size:clamp(30px,4vw,52px);line-height:1.12;margin:14px 0}header p{max-width:850px;color:#d6e6dd}.downloads{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.downloads a{padding:10px 16px;border-radius:8px;background:#f2f7ef;color:#173f34;font-weight:650;text-decoration:none}.note{background:#fff3d8;border:1px solid #e6d29f;border-radius:12px;padding:18px 22px;margin:22px 0}.note strong{color:#6f4913}.priorities{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:24px 0}.priority{padding:20px;background:white;border:1px solid var(--line);border-radius:12px}.priority .label{font-size:12px;color:var(--soft);text-transform:uppercase;letter-spacing:.08em}.priority h2{font-size:24px;margin:6px 0}.priority p{margin:0;color:var(--soft)}h2{font-size:26px;line-height:1.3;margin:30px 0 16px}.month{margin:25px 0 36px}.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));border-left:1px solid var(--line)}.weekdays{border:0;background:#e6ede7;border-radius:9px 9px 0 0;font-size:12px;font-weight:700}.weekdays div{padding:9px}.day{background:white;min-height:125px;padding:8px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}.day.muted,.day.outside{background:#eaf0e9}.dayno{font-size:13px;color:var(--soft)}.chip{display:block;font-size:11px;line-height:1.35;border-radius:4px;padding:5px;margin-top:5px;text-decoration:none;color:#23473c;background:#e5f0e9}.chip.assessment{background:#fce7d5;color:#793e0d;font-weight:650}.chip.preparation,.chip.release{background:#e7e9fb;color:#434c8b}.legend{font-size:13px;color:var(--soft)}.filters{display:flex;flex-wrap:wrap;align-items:center;gap:12px;background:white;border:1px solid var(--line);border-radius:10px;padding:16px;margin:18px 0;position:sticky;top:8px;z-index:2}select,button{font:inherit;border:1px solid #a9bdb0;background:white;padding:8px 10px;border-radius:6px;color:var(--ink)}.event{display:grid;grid-template-columns:210px 1fr;gap:20px;margin:12px 0;background:white;border:1px solid var(--line);border-left:4px solid #8fac9d;border-radius:9px;padding:20px}.event.assessment{border-left-color:#c87525}.event[hidden]{display:none}.date{font-size:14px;font-weight:650}.tag{font-size:11px;color:var(--soft);text-transform:uppercase;letter-spacing:.08em}h3{font-size:18px;line-height:1.35;margin:5px 0 9px}.event p{font-size:14px;color:var(--soft);margin:6px 0}.event .certainty{font-size:12px;font-weight:650;color:#836128}.links,a{color:var(--accent)}.links{font-size:12px}.watch{background:#fff;border:1px solid var(--line);padding:14px 28px;border-radius:12px}.watch li{margin:14px 0}.watch p{font-size:14px;color:var(--soft);margin:4px 0}footer{color:var(--soft);font-size:13px;padding-top:25px}.count{font-size:12px;color:var(--soft);margin-left:auto}@media(max-width:850px){main{padding:16px}header{padding:24px}.priorities{grid-template-columns:1fr}.day{padding:4px;min-height:95px}.chip{font-size:9px;padding:3px}.event{grid-template-columns:1fr;gap:7px}.filters{position:static}}@media print{main{max-width:none;padding:0}body{font-size:10pt}header{background:none;color:black;padding:0}header p,.eyebrow{color:#333}.downloads,.filters,button{display:none}.event{break-inside:avoid}.day{min-height:90px}.month{break-inside:avoid}a{color:inherit}.watch{break-before:page}.priorities{margin:12px 0}.note{margin:10px 0}}
</style><main><header><div class="eyebrow">UCL · Computer Science · Team 21</div><h1>Your next few weeks,<br>in one place.</h1><p>13 November–18 December 2026, plus the required IPAC submission on 23 December. UK time throughout. Checked against Moodle pages, assignment listings, course calendars, announcements and assessment briefs on 13 November.</p><nav class="downloads"><a href="term1-calendar.ics" download>Download main calendar</a><a href="assessments-only.ics" download>Assessments only</a><a href="optional-support.ics" download>Optional support</a><a href="term1-schedule.md">Full readable notes</a></nav></header>
<div class="note"><strong>Two things to keep in view:</strong> the C coursework is due <strong>18 November at 16:00</strong>, and Tetris is due <strong>25 November at 23:59</strong>. The Haskell in-class test and maths exam/mock dates still need confirming. This is a snapshot; it does not update automatically.</div>
<div class="priorities"><div class="priority"><div class="label">First deadline</div><h2>18 Nov · 16:00</h2><p>C maze coursework · 5%<br>Moodle reports “new”, not submitted.</p></div><div class="priority"><div class="label">Next assessed project</div><h2>25 Nov · 23:59</h2><p>Tetris autoplayer · 20%<br>Submit through GitLab / grading server.</p></div><div class="priority"><div class="label">Start the writing</div><h2>4 Dec · 14:00</h2><p>Social Impact Report · 10%<br>Template, 1,200 words maximum + declaration.</p></div></div>
<p class="legend">Orange = assessment or deadline · Green = published teaching or milestone · Purple = preparation or release. The month grids show the main calendar. Date-only markers have no invented cutoff; see the agenda for details.</p>
__MONTHS__
<h2 id="agenda">Agenda and source notes</h2><p>Import the main calendar <em>or</em> assessments-only; the main file already contains the assessments. Optional support can be imported separately. COMP0002 and COMP0147 personal lecture/lab/PBL slots still need to be added from your UCL timetable.</p>
<div class="filters"><label>Show <select id="kind"><option value="main">Main calendar</option><option value="assessments">Assessments only</option><option value="optional">Optional support and events</option><option value="all">Everything</option></select></label><label>Course <select id="course"><option value="all">All courses</option>__COURSES__</select></label><button onclick="window.print()">Print / save PDF</button><span class="count" id="count" aria-live="polite"></span></div>
<div id="events">__CARDS__</div><h2>Still to confirm</h2><div class="watch"><ul>__WATCH__</ul></div>
<footer><p>The full notes include earlier submissions, stale-date conflicts, every source limitation and the review method. Review new announcements weekly. No calendar account has been changed.</p><p><a href="term1-schedule.md">Full notes and earlier-work checks</a> · <a href="events.json">Structured events</a> · <a href="sources/moodle-snapshot-2026-11-13.json">Moodle source snapshot</a></p></footer></main>
<script>const kind=document.getElementById('kind'),course=document.getElementById('course');function filter(){let count=0;document.querySelectorAll('.event').forEach(e=>{const mode=kind.value,optional=e.dataset.optional==='true';const visible=(mode==='all'||mode==='main'&&!optional||mode==='optional'&&optional||mode==='assessments'&&e.dataset.kind==='Assessment')&&(course.value==='all'||course.value===e.dataset.course);e.hidden=!visible;if(visible)count++});document.getElementById('count').textContent=count+' entries';}kind.addEventListener('change',filter);course.addEventListener('change',filter);filter();</script></html>'''
payload=payload.replace('__MONTHS__',''.join(months)).replace('__COURSES__',course_options).replace('__CARDS__',''.join(cards)).replace('__WATCH__',watch)
payload=payload.replace('13 November–18 December 2026','15 November–18 December 2026')
payload=payload.replace('on 13 November.</p>', 'on 15 November, including the accessible lecture slides and notes.</p>')
payload=payload.replace('The Haskell in-class test and maths exam/mock dates still need confirming.', '<strong>Haskell test: 14 December is classmate-reported and UNCONFIRMED; its 5% weight is verified.</strong> Maths is 100% exam-assessed; the exam/mock dates still need confirming.')
payload=payload.replace('<h2 id="agenda">', '<div class="note"><strong>Re-audit complete:</strong> the updated calendar includes an explicitly tentative Haskell marker on 14 December. The Engineering Challenges demo is confirmed on that date, but its Team 21 slot is still unknown. <a href="audit-2026-11-15/audit-report.md">Read the findings and coverage limits</a>.</div><h2 id="agenda">')
payload=payload.replace('Moodle reports “new”, not submitted.', 'Moodle rechecked 15 Nov: “new”, not submitted.')
payload=payload.replace('<a href="term1-schedule.md">Full notes and earlier-work checks</a>', '<a href="audit-2026-11-15/audit-report.md">15 November audit and source coverage</a> · <a href="term1-schedule.md">Full notes and earlier-work checks</a>')
(ROOT/'term1-schedule.html').write_text(payload,encoding='utf-8')

# Keep the reading view aligned with the deeper audit, preserving the earlier
# submission-history dates instead of relabelling old checks as current.
schedule=(ROOT/'term1-schedule.md').read_text(encoding='utf-8')
schedule=schedule.replace('## Assessment deadlines and demonstrations','## Assessment deadlines and demonstrations (includes one unconfirmed date)')
schedule=schedule.replace('- [Assessments only](assessments-only.ics)', '- [Assessments only, including the unconfirmed Haskell marker](assessments-only.ics)\n- [Only assessments with published dates, excluding the classmate-reported Haskell date](published-assessments.ics)')
schedule=schedule.replace('5. **Confirm the Haskell test date with Dr David Clark tomorrow, 16 November.**','5. **Confirm the Haskell test date with Dr David Clark at the first Haskell session on 16 November.**')
schedule=schedule.split('## What was checked and the limits')[0]+'''## What was checked and the limits

The full [15 November re-audit](audit-2026-11-15/audit-report.md) records the evidence, conflicting dates, assessment inventory, next actions and access limitations. It supersedes the narrower 13 November review.

- Reviewed 13 current/support course outlines and their current assignment/quiz listings; read 140 full sections, 47 Page activities and recent discussion excerpts from 17 standard forums. Eight Books were requested; seven blocked chapter text.
- Audited 237 file-list entries: 197 provided reviewable text and one welcome-events image was visually reviewed. The other entries were blocked, oversized, recordings or unsupported formats. Also checked 19 embedded file entries, nine linked GitHub documents and 37 local document copies (overlap included).
- Every exposed programming PDF, including Slides 1 and Module Introduction, was checked for the reported Haskell date. No written confirmation of 14 December was found. The 5% weighting is confirmed by Slides 1, page 8. Recordings and spoken announcements were not comprehensively transcribed.
- The official 2026/27 COMP0147 catalogue confirms 100% Exam, but no exam booking. ENGF0034’s opening lecture places ethics, presentations and scenarios in Term 2.
- C coursework, proposal/criteria and upcoming report submission statuses were rechecked on 15 November. Other earlier-work history remains explicitly dated to the 13 November check. Saved work or a `new` status is not the same as a submitted assignment.
- Personal timetable, extension records, full hsuforum discussions, external GitLab submission state and personal bookings remain unverified. Check the source activity for updates. The older Engineering Challenges 25/26 enrolment and other-programme MATH guidance were excluded.
- [Exact file coverage and failures](audit-2026-11-15/resource-coverage.md) · [Audit summary](audit-2026-11-15/audit-summary.json) · [Original 13 November Moodle snapshot](sources/moodle-snapshot-2026-11-13.json) · [Current structured event data](events.json).

This is a local snapshot; no calendar account was changed. Replace the earlier imported calendar instead of adding this revised copy alongside it to avoid duplicates. Keep the Haskell marker tentative until the date is confirmed.
'''
(ROOT/'term1-schedule.md').write_text(schedule,encoding='utf-8')
print(json.dumps({'core_events':len(CORE),'assessments':len(ASSESSMENTS),'optional_events':len(OPTIONAL),'output':str(ROOT)},indent=2))
