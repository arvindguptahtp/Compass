const chalk = require('chalk')
const hasProps = obj => Object.keys(obj).length > 0 && obj.constructor === Object
const isEmpty = obj => Object.keys(obj).length === 0 && obj.constructor === Object
const isObject = item => (item && typeof item === 'object' && !Array.isArray(item) && item !== null)
const runner = (base, extender, func) => {
    let output = Object.assign({}, base)

    if (isObject(base) && isObject(extender)) {
        Object.keys(extender).forEach(
            key => {
                func(key, output)
            }
        )
    }

    return output
}

let vefas = []
let current = {}
let bus = []
let injector = new Map()

const log = {
    warn (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgYellowBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    err (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgRedBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    impt (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgBlueBright.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    },
    info (header, msg) {
        console.log(
            `\n\n`,
            chalk`{bold.bgCyan.black ${ header }:}`,
            `\n`,
            msg,
            `\n\n`
        )
    }
}


const assign_$inject = function (vefa_obj) {
    if (vefa_obj.$inject) {
        vefa_obj.$inject.forEach(
            (val) => {
                if (injector.has(val)) {
                    vefa_obj[val] = injector.get(val)
                    if (typeof vefa_obj[val] == "function" ) {
                        // vefa_obj[val] = vefa_obj[val].call(vefa_obj)

                    }
                }
            }
        )
    }
}
const assign_$data = function (vefa_obj) {
    if (hasProps(vefa_obj.$data)) {
        Object.keys(vefa_obj.$data).forEach( (key) => {
            // will aways override

            Object.defineProperty(
                vefa_obj,
                key,
                {
                    get: () => {
                        return vefa_obj.$data[key]
                    },
                    set: (val) => {
                        vefa_obj.$data[key] = val
                        assign_$computed(vefa_obj)
                    },
                    configurable: true,
                    enumerable: true
                }
            )
        })
    }
}
const assign_$methods = (vefa_obj) => {
    if (hasProps(vefa_obj.$methods)) {
        Object.keys(vefa_obj.$methods).forEach( (key) => {
            
            try {
                // if (vefa_obj[key] && vefa_obj[key] !== vefa_obj.$methods[key]) {
                //     throw new Error('Vefa Object Method Assignment')
                // }

                // vefa_obj[key] = vefa_obj.$methods[key]
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        value: vefa_obj.$methods[key],
                        writeable: true,
                        configurable: true,
                        enumerable: true
                    }
                )
            }
            catch (ex) {
                console.log(
                    `\nVefa Object method '${ key }' has already been assigned, 
                    please rename.\n`
                )
            }
        })
    }
}
const assign_$options = (vefa_obj) => {
    if (hasProps(vefa_obj.$options)) {
        Object.keys(vefa_obj.$options).forEach( (key) => {
            
            try {
                // if (vefa_obj[key] && vefa_obj[key] !== vefa_obj.$options[key]) {
                //     throw new Error('Vefa Object Options Assignment')
                // }
                // vefa_obj[key] = vefa_obj.$methods[key]
                Object.defineProperty(
                    vefa_obj,
                    key,
                    {
                        get: () => {
                            return vefa_obj.$options[key]
                        },
                        set: (val) => {
                            vefa_obj.$options[key] = val
                            assign_$computed(vefa_obj)
                        },
                        configurable: true,
                        enumerable: true
                    }
                )
            }
            catch (ex) {
                console.log(
                    `Vefa Object option ${ key } has already been assigned, 
                    please rename.`
                )
            }
        })
    }
}
const assign_$computed = (vefa_obj) => {
    if (hasProps(vefa_obj.$computed)) {
        Object.keys(vefa_obj.$computed).forEach( (key) => {
            Object.defineProperty(
                vefa_obj,
                key,
                {
                    value: vefa_obj.$computed[key].call(vefa_obj),
                    writeable: true,
                    configurable: true,
                    enumerable: true
                }
            )
        })
    }
}
const initialize_$members = (vefa_obj, obj) => {
    let seed = Object.assign({}, obj)
    
    if (seed.provide) {
        seed.provide.forEach(
            (tuple) => {
                if (typeof tuple[1] == "function" ) {
                    injector.set(        
                        tuple[0], 
                        tuple[1].call(seed)
                    )
                }
                else {
                    injector.set(
                        tuple[0], 
                        tuple[1]
                    )
                }
            }
        )
    }

    Object.defineProperty(
        vefa_obj,
        '$data',
        {
            value: seed.data || {},
            writable: true,
            configurable: false,
            enumerable: true
        }
    )
    
    Object.defineProperty(
        vefa_obj,
        '$methods',
        {
            value: seed.methods || {},
            writable: true,
            configurable: false,
            enumerable: true
        }
    )
    
    Object.defineProperty(
        vefa_obj,
        '$computed',
        {
            value: seed.computed || {},
            writable: true,
            configurable: false,
            enumerable: true
        }
    )

    Object.defineProperty(
        vefa_obj,
        '$inject',
        {
            value: seed.inject || [],
            writable: true,
            configurable: false,
            enumerable: true
        }
    )

    clean_seed(seed)
    
    // set the remainder items to $options for later weaving
    Object.defineProperty(
        vefa_obj,
        '$options',
        {
            value: seed || {},
            writable: true,
            configurable: false,
            enumerable: true
        }
    )

    seed = {}
}

const clean_seed = (seed) => {
    [
        "class", "data", "methods", "computed", "provide", "inject", "options",
        "$data", "$methods", "$computed", "$inject", "$options",
    ].forEach(
        (type) => {
            if (seed[type]) {
                delete seed[type]
            }
        }
    )
}

const replace_with = (base, extender) => {
    return runner(base, extender, (key, output) => {
        if (isObject(extender[key])) {
            if (!(key in base)) {
                Object.assign(output, { [key]: extender[key] })
            }
            else {
                output[key] = replace_with(base[key], extender[key])
            }
        }
        else {
            Object.assign(output, { [key]: extender[key] })
        }
    })
}
const merge = (base, extender) => {
    return runner(base, extender, (key, output) => { 
        if (key == "data") {
            throw console.log("You can not mix a Vefa data object, please create or define")
        }
        if (isObject(extender[key])) {
            if (!(key in base)) {
                Object.assign(output, { [key]: extender[key] })
            }
            else {
                output[key] = merge(base[key], extender[key])
            }
        }
        else {
            if (!(key in base)) {
                Object.assign(output, { [key]: extender[key] })
            }
            else {
                if (base[key]){
                    if ( !(base[key].includes(extender[key])) ) {
                        Object.assign(output, { [key]: `${base[key]} ${extender[key]}` })
                    }
                }
                else {
                    Object.assign(output, { [key]: extender[key] })
                }
            }
        }
    })
}
const remove_values = (base, extender) => {
    return runner(base, extender, (key, output) => { 
        if (key == "data") {
            throw console.log("You can not remove a Vefa data object, please create or define")
        }   
        
        console.log(base)
        console.log(extender)

        if (isObject(extender[key])) {
            if (key in base) {
                output[key] = remove_values(base[key], extender[key])
            }
        }
        else {
            if (key in base) {
                if (base[key]){
                    base[key] = base[key].split(" ").filter(
                        (value) => {
                            return extender[key].split(" ").indexOf(value) == -1
                        }
                    ).join(" ")

                    Object.assign(output, {[key]: base[key]})
                }
            }
        }
    })
}



class Vefa {
    constructor (obj = {}) {
        let is_included = (element) => { return obj.class === element.class }

        // require a name
        try {
            if (!obj) {
                throw new Error(`"VEFA Instantion Error: Vefa object missing\n`)
            }
            if (!obj.class) {
                throw new Error(
                    `"VEFA Instantion Error: Vefa object missing class designation\n
                    ${ JSON.stringify(obj) }`
                )
            }
        
            // get rid of those random null objs that seem to come in for some reason (webpack?)
            if (vefas.find(is_included)) { 
                return vefas.find(is_included)
            }

            let seed = Object.assign({}, obj)
            
            // get class as special, we don't want to be able to reassing it later.
            Object.defineProperty(
                this,
                'class',
                {
                    value: seed.class || 'vefa-object',
                    configurable: true,
                    writable: true,
                    enumerable: true
                }
            )
            
            // this will be locally assigned to the view for ease of "thinking"
            Object.defineProperty(
                this,
                '_view',
                {
                    value: seed.class.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase() }) || 'vefa',
                    configurable: true,
                    writable: true,
                    enumerable: true
                }
            )
            initialize_$members(this, seed)
            
            this.vefa_id = Vefa.add(this)
            return this
        }
        catch (ex) {
            console.log(chalk.red.bold(ex.message))
        }
    }
    define (obj) {
        let local_name = this.class
        
        if (arguments[1]) {
            local_name = arguments[0]
            obj = arguments[1]
        }

        if (local_name == this.class) {
            let seed = Object.assign({}, obj)

            // we're extending an abstract and want a new class name
            
            this.class = (seed.class) ? seed.class : this.class
            this.$data = replace_with(this.$data, seed.data || {})
            this.$methods = replace_with(this.$methods, seed.methods || {})
            this.$computed = replace_with(this.$computed, seed.computed || {})
            clean_seed(seed)
            this.$options = replace_with(this.$options, seed || {})
            
            seed = {}
            
            return this
        }
    }
    mixin (obj) {
        let local_name = this.class
        
        if (arguments[1]) {
            local_name = arguments[0]
            obj = arguments[1]
        }

        if (local_name == this.class) {
            let seed = Object.assign({}, obj)

            // can't merge name
            // lets figure out how to merge methods and computed (but not now!)
            // should be able to mixin a data member if its not there.
            // but we only care about options for now.
            delete seed.class
            delete seed.data
            delete seed.methods
            delete seed.computed

            this.$options = merge(this.$options, seed || {})

            return this
        }
    }
    data (obj) {
        let local_name = this.class
        
        if (arguments[1]) {
            local_name = arguments[0]
            obj = arguments[1]
        }

        if (local_name == this.class) {
            this.$data = replace_with(this.$data, obj || {})
            // this.$weave() don't weave until mounting
            return this
        }
    }
    set_data (obj) { return this.data(obj) }
    remove_opts (obj) {
        // we only want to worry about options for now
        let seed = Object.assign({}, obj)
        delete seed.class
        delete seed.data
        delete seed.methods
        delete seed.computed

        this.$options = remove_values(this.$options, seed || {})

        return this
    }

    static vefas () { return vefas }
    static add (vefa) { return vefas.push(vefa) }
    static remove (id) { vefas = vefas.filter( (item) => item.id !== id ) }

    static set_current (cur) { if (cur instanceof Vefa) current = cur }
    static get_current () { return current }

    static set_bus (id, val) { bus[id] = val }
    static has_bus(id) { if(bus[id]) return true }
    static $view_bus () { return bus }
    static get_bus (id, to_remove) {
        // silent fail because pre-render run-thoughs by webpack (?)
        // catch no id but do not harm output
        if(!bus[id]) { return } 
        let val = bus[id]
        if (to_remove) delete bus[id]
        return val
    }
    static remove_bus (id) {
        // silent fail because pre-render run-thoughs by webpack (?)
        // catch no id but do not harm output
        if(!bus[id]) { return } 
        delete bus[id]
    }

    static run_lifecycle (vefa, cycle) {
        if (vefa["$options"] && typeof vefa["$options"][cycle] == 'function') {
            Vefa.$weave(vefa)
            vefa["$options"][cycle].call(vefa)
            Vefa.$proxy_back(vefa)
        }
    }
    static $inject () {}
    static $weave (vefa) {
        // do something with inject
        if (isObject(vefa) && vefa instanceof Vefa) {
            assign_$inject(vefa)
            assign_$data(vefa)
            assign_$methods(vefa)
            assign_$options(vefa)
            assign_$computed(vefa)
        }
        
    }

    static $proxy_back (vefa) {
        let seed = Object.assign({}, vefa)
        // methods and computed don't "change"
        // data and options might!
        Object.keys(seed).forEach(
            (prop) => {
                if (prop in Object.keys(vefa.$data)) {
                    vefa.$data[prop] = seed[prop]
                }
                if (prop in Object.keys(vefa.$options)) {
                    vefa.$options[prop] = seed[prop]
                }
            }
        )
    }

    static $unravel (vefa) {
        if (vefa.provide) {
            vefa.provide.forEach( tuple => injector.delete(tuple[0]) )
        }
        Vefa.remove(vefa.id)
        vefa = {}
    }

    static $dump (obj, msg) {
        log.info(`${ (msg) ? msg : "VEFA DUMP" }:`, obj)
    }
}


module.exports = Vefa
