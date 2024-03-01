<script>
  import HighChart from './HighChart.svelte';
  import { onMount } from 'svelte';
  import api from '$lib/api';

  onMount(async () => {
    const symbols = await api.v1.symbols.get();
    console.log(symbols);
  });
</script>

<div class="w-full h-full">
  <HighChart />
</div>
