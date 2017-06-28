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

module.exports = class Vefa {
    constructor (obj = {}) {
        this._mixin = {}
        this._abstract = {
            data: {}
        }
        this._instance = {
            data: {}
        }
        this._extend = {
            data: {}
        }
        this._data = {}
        this._labels = {}

        this.define(obj)

        return this
    }

    //- initialize the abstract
    define (obj) {
        if (hasProps(obj)) {
            this._abstract = this.replace_with(this._abstract, obj)
        }

        return this
    }

    //- initialize the _mixin
    mix (obj) {
        if (hasProps(obj)) {
            this._mixin = this.merge(this._mixin, obj)
        }

        return this
    }

    //- initialize the current instance
    replace (obj) {
        if (hasProps(obj)) {
            this._instance = this.replace_with(this._instance, obj)
        }

     
        return this
    }

    //- initialize the _mixin
    mixin (obj) {
        if (hasProps(obj)) {
            this._mixin = this.merge(this._mixin, obj)
        }

        return this
    }

    //- initialize the current instance
    instance (obj) {
        if (hasProps(obj)) {
            this._instance = this.replace_with(this._instance, obj)
        }

        return this
    }

    //- initialize the current instance
    //- meant for the outermost layer, called before an include
    extend (obj) {
        if (hasProps(obj)) {
            this._extend = this.replace_with(this._extend, obj)
        }

        return this
    }

    // syntactic sugar as "create" after the abstract is linguistic error
    presets (obj) {
        this.define(obj)
    }

    // helper function
    data (obj) {
        if (hasProps(obj)) {
            this._data = this.replace_with(this._data, obj)
        }

        return this
    }

    // helper function
    labels (obj) {
        if (hasProps(obj)) {
            this._labels = this.replace_with(this._labels, obj)
        }

        return this
    }
    
    //- iteratively and recursively go through object and share property values
    merge (base, extender) {
        return runner(base, extender, (key, output) => { 
            if (key == "data") {
                throw console.log("You can not mix a Vefa data object, please create or define")
            }
            if (isObject(extender[key])) {
                if (!(key in base)) {
                    Object.assign(output, { [key]: extender[key] })
                }
                else {
                    output[key] = this.merge(base[key], extender[key])
                }
            }
            else {
                if (!(key in base)) {
                    Object.assign(output, { [key]: extender[key] })
                }
                else {
                    if (base[key]){
                        Object.assign(output, { [key]: `${base[key]} ${extender[key]}` })
                    }
                    else {
                        Object.assign(output, { [key]: extender[key] })
                    }
                }
            }
        })
    }

    //- iteratively and recursively go through object and override property values
    replace_with (base, extender) {
        return runner(base, extender, (key, output) => {
            if (isObject(extender[key])) {
                if (!(key in base)) {
                    Object.assign(output, { [key]: extender[key] })
                }
                else {
                    output[key] = this.replace_with(base[key], extender[key])
                }
            }
            else {
                Object.assign(output, { [key]: extender[key] })
            }
        })
    }

    static $thaw (vefa) {
        if (vefa.$ghost) {
            vefa = vefa.$ghost
            
        }        
    }

    // create a plain object that we can use
    $freeze (obj = this._abstract) {
        let factory = {
        	$ghost: this,
          	$thaw () { return this.$ghost },
            data: {},
            labels: {}
        }

        if (!obj) { obj = {} }
        
        factory = this.replace_with(obj.extends ? obj.extends : obj, factory)
        
        //- add properties
        factory = (obj.mixin && hasProps(obj.mixin))
            ? this.merge(factory, obj.mixin)
            : factory = this.merge(factory, this._mixin)

        //- overwrite properties
        factory = (obj.instance && hasProps(obj.instance))
            ? this.replace_with(factory, obj.instance)
            : this.replace_with(factory, this._instance)

        //- overwrite properties
        factory = (this._extend && hasProps(this._extend))
            ? this.replace_with(factory, this._extend)
            : factory

        factory.data = this.replace_with(factory.data, this._data)
        factory.labels = this.replace_with(factory.labels, this._labels)
        
        return factory
    }
}
