<script>
  import ChartContainer from '$lib/components/Chart/Container.svelte';
  import SymbolList from '$lib/components/Common/SymbolList.svelte';
</script>

<div class="flex w-full h-full">
  <ChartContainer />
  <div class="w-fit max-w-[300px] h-full">
    <SymbolList />
  </div>
</div>
