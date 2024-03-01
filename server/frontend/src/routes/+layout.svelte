<script>
  import '../app.css';
  import Sidebar from '$lib/components/Common/Sidebar/Container.svelte';
</script>

<div class="flex h-full">
  <Sidebar />
  <slot />
</div>
