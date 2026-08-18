# UD Accounting Hoop Challenge Leaderboard

The game uses a public Google Form submission endpoint and a published,
formula-generated Google Sheets leaderboard. No Google password, API key, or
service-account credential is stored in this repository.

## Google resources

- Form: [UD Accounting Hoop Challenge Leaderboard](https://docs.google.com/forms/d/1vhCUSfIOpvp4h1kyaAQmtqhsq0_aI4ioO_ialiYOaAE/edit)
- Response Sheet: [UD Accounting Hoop Challenge Leaderboard (Responses)](https://docs.google.com/spreadsheets/d/17p8DJYHKFRHzcp_DX_QMPszYgUbirOZ3c2AYNnX-DGA/edit?gid=183002363)
- Public leaderboard CSV: `https://docs.google.com/spreadsheets/d/e/2PACX-1vQtNnYVM9mU7X63VhPlng78CqwawCLIXHqIREAZawATyZEhsEWs_6TI_b8KK4hRC_zeiKwxaL1R72bg/pub?gid=4392995&single=true&output=csv`

The Form records First Name, Last Initial, Section Number, Score, a hidden
Attempt ID, and completion time in seconds. Email collection and Google sign-in
are disabled.

## High-score calculation

The private `Form Responses 1` tab contains every attempt. The `Leaderboard`
tab uses this formula in cell A1:

```text
=LET(names,FILTER('Form Responses 1'!B2:B,'Form Responses 1'!B2:B<>""),initials,FILTER('Form Responses 1'!C2:C,'Form Responses 1'!B2:B<>""),sections,FILTER('Form Responses 1'!D2:D,'Form Responses 1'!B2:B<>""),scores,FILTER('Form Responses 1'!E2:E,'Form Responses 1'!B2:B<>""),times,FILTER('Form Responses 1'!G2:G,'Form Responses 1'!B2:B<>""),players,UNIQUE(HSTACK(names,initials,sections)),highScores,MAP(CHOOSECOLS(players,1),CHOOSECOLS(players,2),CHOOSECOLS(players,3),LAMBDA(n,i,s,MAX(FILTER(scores,names=n,initials=i,sections=s)))),bestTimes,MAP(CHOOSECOLS(players,1),CHOOSECOLS(players,2),CHOOSECOLS(players,3),highScores,LAMBDA(n,i,s,h,IFERROR(MIN(FILTER(times,names=n,initials=i,sections=s,scores=h,times<>"")),""))),leaders,HSTACK(players,highScores,bestTimes,IF(bestTimes="",1,0)),sorted,SORT(leaders,4,FALSE,6,TRUE,5,TRUE),VSTACK({"First Name","Last Initial","Section","High Score","Best Time (seconds)"},CHOOSECOLS(sorted,1,2,3,4,5)))
```

The formula keeps one row per first-name/last-initial/section identity. It finds
the student's highest score, selects the fastest time only from attempts that
earned that score, then sorts by score descending and time ascending. Legacy
attempts without completion time sort behind timed attempts when scores tie.

Only the calculated `Leaderboard` tab is published. The raw response tab stays
private. The synthetic setup check (`Test S.`, section `999`) is filtered from
the in-app table.

## Operational notes

- Google can take a few seconds to refresh the published table after a Form
  submission. The completion view includes a Refresh button.
- Identity is intentionally lightweight: first name + last initial + section.
  Students with identical values share one displayed high-score identity.
- The score is generated in the browser and is appropriate for a casual class
  activity, not a tamper-proof graded assessment.
