<script>
  import SymbolList from './lib/components/SymbolList.svelte';
  import symbols from '$lib/stores/symbols';
</script>

<div class="flex w-full h-full">
  <!-- <ChartContainer symbol={$symbol} /> -->
  <div class="w-fit max-w-[300px] h-full">
    <SymbolList symbols={$symbols} />
  </div>
</div>
