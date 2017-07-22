module.exports = {
    clean_seed (seed) {
        [
            "class", "data", "methods", "computed", "dom", "provide", "inject", "options",
            "$data", "$methods", "$computed", "$dom", "$inject", "$options",
        ].forEach(
            (type) => {
                if (seed[type]) {
                    delete seed[type]
                }
            }
        )
    }
}
