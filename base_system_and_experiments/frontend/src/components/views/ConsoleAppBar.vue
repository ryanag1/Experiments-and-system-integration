<template>
    <v-app-bar color="black" dark app clipped-left clipped-right dense>
        <v-app-bar-nav-icon @click="$emit('drawer-icon-click');"></v-app-bar-nav-icon>
        
        <v-toolbar-title>Myapp Console</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-spacer></v-spacer>

        <server-status-menu-button :duct="duct"></server-status-menu-button>

    </v-app-bar>
</template>

<script>
import ServerStatusMenuButton from './ConsoleServerStatusMenuButton'

export default {
    components: {
        ServerStatusMenuButton
    },
    data: () => ({
        rules: null

    }),
    props: ["duct"],
    methods: {
        
    },
    watch: {
    
    },
    created() {
        this.duct.invokeOrWaitForOpen(() => {
            
        });
    }
}
</script>