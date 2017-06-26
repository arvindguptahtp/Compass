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

            slot(
                v-if="fold"
                name="icon-open"
            )
            slot(
                v-if="!fold"
                name="icon-close"
            )
    
    slot(
        name="bd"
        v-if="!fold"
    )

</template>
