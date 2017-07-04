<script>
    export default {
        name: 'fold-unfold',
        props: {
            init: Boolean,
            title: String,
            styles: String
        },
        data () {
            return {
                fold: this.init || false
            }
        },
        methods: {
            update (ev) {
                this.fold = !this.fold
                ev.target.blur()
            }
        },
        computed: {
            menu_icon () {
                if (this.fold) {
                    return "#ico--menu"
                }
                else {
                    return "#ico--menu-close"
                }
            }
        }
    }
</script>


<template lang="pug">
fieldset
    header
        button(
            type="button"
            @click="update"
            class="fm-fieldset-legend",
            :class="[styles, {'is-active': !fold}]"
            o-base="row--pGrid--sMiddle mod--balance pad--x25 pad--y25 rhy--xStart25",
            o-standard="pad--x100"
        )
            span(v-text="title")

            svg.ico
                use(:href="menu_icon")
    
    div(v-show="!fold")
        slot(
            name="bd"
        )

</template>
