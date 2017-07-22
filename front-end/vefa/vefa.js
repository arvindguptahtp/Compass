const _ = require('./lib/verify')
const log = require("./lib/reporter")
const convert = require('./lib/convert')
const django = require('./lib/django')({django: true})

const inits = require("./framework/initializers")
const assign = require("./framework/assigners")
const teardowns = require('./framework/teardowns')

let vefas = []
let current = {}
let injector = new Map()

class Vefa {
    constructor (name, obj = {}) {
        // require a name
        try {
            if (!name || typeof name != "string") {
                throw new Error(`VEFA Instantion Error: Vefa declaration missing name designation`)
            }
       
            // get rid of those random null objs that seem to come in for some reason (webpack?)
            let is_included = (element) => { return name === element.class }
            if (vefas.find(is_included)) { 
                return vefas.find(is_included)
            }

            
            let seed = Object.assign({}, obj)
            // get class as special, we don't want to be able to reassing it later.
            Object.defineProperty(
                this,
                'class',
                {
                    value: name,
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
                    value: name.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase() }) || 'vefa',
                    configurable: true,
                    writable: true,
                    enumerable: true
                }
            )
            inits.initialize_$members(this, seed)
            
            this.vefa_id = Vefa.add(this)

            // log.info("Vefa", this)
            return this
        }
        
        catch (ex) {
            log.err("error", ex.message)
        }
    }

    // Replace default or abstract data for the subclass or instance
    // Replaces data objects wholesale
    data (obj = {}) {
        this.$data = Object.assign(this.$data, obj)
        return this
    }

    methods (obj = {}) {
        this.$methods = Object.assign(this.$methods, obj)
        return this
    }

    computed (obj = {}) {
        this.$computed = Object.assign(this.$computed, obj)
        return this
    }

    options (obj = {}) {
        this.$options = Object.assign(this.$options, obj)
        return this
    }

    dom (obj = {}) {
        // if we send an array to the function,
        // we're setting up placeholders for use in the template
        if (Array.isArray(obj)) {
            let placeholders = {}
            obj.forEach(
                (item) => placeholders[item] = {class:""}
            )
            obj = placeholders
        }
        this.$dom = Object.assign(this.$dom, convert.arrize(obj))
        
        return this
    }

    apply (name) {
        return (this._view == name) ? this : new Vefa("garbage_collect")
    }

    define (name, obj) {
        // we're extending an abstract and we may want a new class name
        this.class = (name && !_.is_object(name)) ? name : this.class
        obj = (!obj) ? name : obj
        
        if (_.is_object(obj)) {
            this.data(obj.data)
            this.methods(obj.methods)
            this.computed(obj.computed)
            this.dom(obj.dom || {})
            
            teardowns.clean_seed(obj)
            
            this.options(obj)
        }
        
        obj = {}
        
        return this
    }
    // syntactic sugar
    subclass (name, obj) { return this.define(name, obj) }
    variant (name, obj) { return this.define(name, obj) }
    instance (name, obj) { return this.define(name, obj) }

    dom_mix (mix_obj) {
        let dom_obj = this.$dom
        mix_obj = convert.arrize(mix_obj)
        
        Object.keys(mix_obj).forEach(
            (element) => {
                // ex: $dom.element
                if (dom_obj[element]) {
                    let mix_element = mix_obj[element]
                    let dom_element = dom_obj[element]
                    
                    Object.keys(mix_element).forEach(
                        (attr) => {
                            // ex: $dom.element.class || $dom.element["o-base"]
                            if (dom_element[attr]) { 
                                let mix_attr = mix_element[attr]
                                // create a copy that we can alter and reassign to the real dom_element[attr]
                                let dom_attr = dom_element[attr]

                                if (Array.isArray(dom_attr)) {
                                    dom_element[attr] = dom_attr.concat(mix_attr)
                                }
                            
                            }
                            else {
                                dom_element[attr] = mix_element[attr]
                            }
                        }
                    )
                }
                else {
                    dom_obj[element] = mix_obj[element]
                }
            }
        )
        
        return this
    }

    dom_switch (mix_obj) {
        let dom_obj = this.$dom
        
        Object.keys(mix_obj).forEach(
            (element) => {
                // ex: $dom.element
                if (dom_obj[element]) {
                    let mix_element = mix_obj[element]
                    let dom_element = dom_obj[element]

                    Object.keys(mix_element).forEach(
                        (attr) => {
                            if (dom_element[attr]) {
                                let mix_rm_decs = mix_element[attr][0].split(" ")
                                let dom_decs = dom_element[attr]
                                
                                dom_element[attr] = dom_decs.filter(
                                    (item) => {
                                        return !mix_rm_decs.includes(item)
                                    }
                                )

                                if (mix_element[attr][1]) {
                                    let mix_add_decs = mix_element[attr][1].split(" ")
                                    dom_element[attr] = dom_element[attr].concat(mix_add_decs)
                                }
                            }
                        }
                    )
                }
                //  else do nothing as it doesn't exist
            }
        )

        return this
    }

    proxy () {
        this.proxied = true
        return this
    }

    echo (hdr = "Current Vefa state", obj = this) {
        obj = (_.is_object(hdr) && obj === this) ? hdr : obj
        hdr = (_.is_object(hdr)) ? "Current Vefa state" : hdr 
        log.impt(hdr, obj)
    }

    static $weave (vefa) {
        if (_.is_object(vefa) && vefa instanceof Vefa) {
            // assign_$inject(vefa)
            assign.$data(vefa)

            if (vefa.key) {
                let key = vefa.key
                let parent = vefa

                String.prototype.io = function () {
                    if (key == this) return this

                    return (parent[this])
                        ? `${key}.${parent[this]}`
                        : `${key}.${this}`
                }

                String.prototype.tag = function ( ...filters ) {
                    let val = (key == this)
                        ? this
                        : this.io()

                    return (filters)
                        ? django.v(val, ...filters)
                        : django.v(val)
                }
            }

            assign.$methods(vefa)
            assign.$options(vefa)
            assign.$computed(vefa)
            assign.$dom(vefa)
        }
    }

    
    
    static vefas () { return vefas }
    static add (vefa) { return vefas.push(vefa) }
    static remove (id) { vefas = vefas.filter( (item) => item.vefa_id !== id ) }
    static vefas_count () { return vefas.length}
    static set_current (cur) { if (cur instanceof Vefa) current = cur }
    static get_current () { return current }
    
    set (item, value) {
        injector.set(item, value)
    }
    get (item) {
        return (injector.has(item))
            ? injector.get(item)
            : false
    }
    has (item) {
        return injector.has(item)
    }
    rm (item) {
        injector.delete(item)
    }
    count () {
        return injector.size
    }

    static proxy (vefa) {
        return new Proxy(
            vefa,
            {
                get: function(target, name) {
                    return name in target 
                        ? target[name]
                        : name
                }
            }
        )
    }

    static run_lifecycle (vefa, cycle) {
        if (vefa["$options"] && typeof vefa["$options"][cycle] == 'function') {
            Vefa.$weave(vefa)
            vefa["$options"][cycle].call(vefa)
            Vefa.$reswift(vefa)
            Vefa.$weave(vefa)
        }
    }
    
    static $reswift (vefa) {
        let seed = Object.assign({}, vefa)
        
        // methods and computed don't "change"
        // data, options, and dom might!
        Object.keys(seed).forEach(
            (prop) => {
                if (prop in Object.keys(vefa.$data)) {
                    vefa.$data[prop] = seed[prop]
                }
                if (prop in Object.keys(vefa.$options)) {
                    vefa.$options[prop] = seed[prop]
                }
                if (prop in Object.keys(vefa.$dom)) {
                    vefa.$dom[prop] = seed[prop]
                }
            }
        )
    }
    
    static $unravel (vefa) {
        // make sure it exsits and if proxied and doesn't exist, lets make sure we ignore it
        if (vefa.provide && vefa.provide !== "provide") {
            console.log(vefa.provide)
            vefa.provide.forEach( tuple => injector.delete(tuple[0]) )
        }
        Vefa.remove(vefa.vefa_id)
        vefa = {}
    }
}

module.exports = Vefa
