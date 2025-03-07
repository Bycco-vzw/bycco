const _st_headers = [
  {
    u_title: "Nb",
    sortable: false,
    value: "rank",
  },
  {
    u_title: "Name",
    sortable: false,
    value: "name",
  },
  {
    title: "ID Bel",
    sortable: false,
    value: "idbel",
  },
  {
    title: "Elo used",
    sortable: false,
    value: "elo",
  },
  {
    u_title: "Points",
    sortable: false,
    value: "points",
  },
  {
    title: "Birth year",
    sortable: false,
    value: "birthyear",
  },
  {
    title: "Gender",
    sortable: false,
    value: "gender",
  },
  {
    title: "Bel. Elo",
    sortable: false,
    value: "ratingbel",
  },
  {
    title: "FIDE Elo",
    sortable: false,
    value: "ratingfide",
  },
  {
    title: "Club ID",
    sortable: true,
    value: "idclub",
  },
  {
    title: "Club name",
    sortable: true,
    value: "clubname",
  },
  {
    u_title: "Games",
    sortable: false,
    small: true,
    value: "ngames",
  },
  {
    title: "BC1",
    sortable: false,
    small: true,
    value: "tb1",
  },
  {
    title: "Buch",
    sortable: false,
    small: true,
    value: "tb2",
  },
  {
    title: "SB",
    sortable: false,
    small: true,
    value: "tb3",
  },
  {
    title: "Prog",
    sortable: false,
    small: true,
    value: "tb4",
  },
  {
    title: "DE",
    sortable: false,
    small: true,
    value: "tb5",
  },
]
const pr_headers = [
  {
    u_title: "Nb",
    sortable: false,
    value: "boardnr",
  },
  {
    u_title: "White",
    sortable: false,
    value: "white",
  },
  {
    u_title: "Result",
    sortable: false,
    value: "result",
  },
  {
    u_title: "Black",
    sortable: false,
    value: "black",
  },
]

function getWhiteResult(rescode) {
  switch (rescode) {
    case "1":
      return "1-0"
    case "0":
      return "0-1"
    case "½":
      return "½-½"
    case "1FF":
      return "1-0 FF"
    case "0ff":
      return "0-1 FF"
    case "-":
      return "-"
  }
}

function processSwarJson(swarjson, t) {
  const standings = [],
    pairings = [],
    sortpairings = []
  const players = swarjson.Swar.Player
  let st_headers = _st_headers
  players.forEach((p) => {
    standings[p.Ranking - 1] = {
      id: p.NationalId,
      rank: p.Ranking,
      name: p.Name,
      elo: Math.max(p.FideElo, p.NationalElo),
      ngames: p.NbOfParts,
      points: parseFloat(p.Points),
      idbel: p.NationalId,
      gender: p.Sex[0],
      tb1: p.TieBreak[0].Points,
      tb2: p.TieBreak[1].Points,
      tb3: p.TieBreak[2].Points,
      tb4: p.TieBreak[3].Points,
      tb5: p.TieBreak[4].Points,
      birthyear: p.BirthDate,
      ratingbel: p.NationalElo,
      ratingfide: p.FideElo,
      idclub: p.ClubNumber,
      clubname: p.ClubName,
    }
    if (!p.RoundArray) p.RoundArray = []
    p.RoundArray.forEach((r) => {
      const rnr = r.RoundNr
      const pr = pairings[rnr] || {
        games: [],
        bye: null,
        absent: [],
        rnr,
      }
      switch (r.Color) {
        case "No Color":
          if (r.Tabel === "BYE") {
            pr.bye = {
              white: p.Name,
              black: "Bye",
              result: "",
            }
          }
          if (r.Tabel === "Absent") {
            pr.absent.push({
              white: p.Name,
              black: t("Absent"),
              result: "",
            })
          }
          break
        case "White":
          let boardnr = parseInt(r.Tabel) - 1
          pr.games.push({
            white: p.Name,
            black: r.OpponentName,
            result: getWhiteResult(r.Result),
            boardnr: boardnr + 1,
          })
          break
      }
      pairings[rnr] = pr
    })
  })
  const maxround = pairings.length - 1
  pairings.forEach((p, ix) => {
    p.games.sort((x, y) => x.boardnr - y.boardnr)
    if (ix > 0) {
      sortpairings[maxround - ix] = {
        games: p.games,
        rnr: p.rnr,
      }
      if (p.bye) {
        sortpairings[maxround - ix].games.push(p.bye)
      }
      if (p.absent) {
        sortpairings[maxround - ix].games.push(...p.absent)
      }
    }
  })
  st_headers.forEach((h) => {
    if (h.u_title) {
      h.title = t(h.u_title)
    }
  })
  pr_headers.forEach((h) => {
    if (h.u_title) {
      h.title = t(h.u_title)
    }
  })
  return { standings, pairings, sortpairings, st_headers, pr_headers }
}

export { processSwarJson }
