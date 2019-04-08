from code.util.db import Submission, User, Contest
from code.generator.lib.htmllib import *
from code.generator.lib.page import *
import logging
from code.util import register
import time

def detailedReport(params, user):
    contest = Contest.getCurrent() or Contest.getPast()
    if not contest:
        return Page(
            h1("&nbsp;"),
            h1("No Contest Available", cls="center")
        )
    elif contest.scoreboardOff <= time.time() * 1000 and not user.isAdmin():
        return Page(
            h1("&nbsp;"),
            h1("Scoreboard is off.", cls="center")
        )

    start = contest.start
    end = contest.end
    
    subs = {}
    for sub in Submission.all():
        if start <= sub.timestamp <= end and not sub.user.isAdmin():
            subs[sub.user.id] = subs.get(sub.user.id) or []
            subs[sub.user.id].append(sub)            
    
    problemSummary = {}
    for prob in contest.problems:
        problemSummary[prob.id] = [0, 0]

    scores = []
    for user in subs:
        usersubs = subs[user]
        scor = score(usersubs, start, problemSummary)
        scores.append((
            User.get(user).username,
            scor[0],
            scor[1],
            scor[2],
            len(usersubs)
        ))
    scores = sorted(scores, key=lambda score: score[1] * 1000000000 + score[2] * 10000000 - score[3], reverse=True)
    
    ranks = [i + 1 for i in range(len(scores))]
    for i in range(1, len(scores)):
        u1 = scores[i]
        u2 = scores[i - 1]
        if (u1[1], u1[2], u1[3]) == (u2[1], u2[2], u2[3]):
            ranks[i] = ranks[i - 1]
    
    subs = {}
    for sub in Submission.all():
        if start <= sub.timestamp <= end and not sub.user.isAdmin():
            subs[sub.user.id] = subs.get(sub.user.id) or []
            subs[sub.user.id].append(sub)

    pn = 0
    probCount = []
    for i in range(len(contest.problems)):
        pn += 1
        probCount.append(h.th(str(pn)))



    i = 0
    for user in subs:
        i += 1
        listOfSubs = subs[user]
        m = 0
        for subm in listOfSubs:
            m += 1

        print(listOfSubs)
    
    finalStandingDisplay = []
    for (name, solved, samples, points, attempts), rank in zip(scores, ranks):
        finalStandingDisplay.append(h.tr(
            h.td(rank, cls="center"),
            h.td(name),
            h.td(User.getByName(name).id, cls="center"),
            h.td(solved, cls="center"),
            h.td(points, cls="center"),
            h.td(attempts, cls="center")
        ))

    problemSummaryDisplay = []

    print("did i get here?")
 
    return Page(
        h2("Final Standings", cls="page-title"),
        h.table(
            h.thead(
                h.tr(
                    h.th("Rank"),
                    h.th("Username", cls="center"),
                    h.th("ID"),
                    h.th("Correct"),
                    h.th("Penalty"),
                    h.th("Attempts"),
                    *probCount
                )
            ),
            h.tbody(
                *finalStandingDisplay
            )
        ),
        h2("Problem Summary", cls="page-title"),
        h.table(
            h.thead(
                h.tr(
                    h.th("Rank"),
                    h.th("Username", cls="center"),
                    h.th("ID"),
                    h.th("Correct"),
                    h.th("Penalty"),
                    h.th("Attempts"),
                )
            ),
            h.tbody(
                *finalStandingDisplay
            )
        )
    )

def score(submissions: list, contestStart, problemSummary) -> tuple:
    """ Given a list of submissions by a particular user, calculate that user's score.
        Calculates score in ACM format. """
    
    solvedProbs = 0
    sampleProbs = 0
    penPoints = 0

    # map from problems to list of submissions
    probs = {}

    # Put the submissions into the probs list
    for sub in submissions:
        probId = sub.problem.id
        if probId not in probs:
            probs[probId] = []
        probs[probId].append(sub)
    
    # For each problem, calculate how much it adds to the score
    for prob in probs:
        # Sort the submissions by time
        subs = sorted(probs[prob], key=lambda sub: sub.timestamp)
        # Penalty points for this problem
        points = 0
        solved = False
        sampleSolved = False
        
        for sub in subs:
            for res in sub.results[:sub.problem.samples]:
                if res != "ok":
                    break
            else:
                sampleSolved = True
            if sub.result != "ok":
                # Unsuccessful submissions count for 20 penalty points
                # But only if the problem is eventually solved
                points += 20
            else:
                # The first successful submission adds a penalty point for each
                #     minute since the beginning of the contest
                # The timestamp is in millis
                points += (sub.timestamp - contestStart) // 60000
                solved = True
                break
        
        # Increment attempts
        problemSummary[sub.problem.id][0] += 1

        # A problem affects the score only if it was successfully solved
        if solved:
            solvedProbs += 1
            penPoints += points
            problemSummary[sub.problem.id][1] += 1
        elif sampleSolved:
            sampleProbs += 1
    
    # The user's score is dependent on the number of solved problems and the number of penalty points
    return solvedProbs, sampleProbs, int(penPoints)

register.web("/detailedReport", "loggedin", detailedReport)