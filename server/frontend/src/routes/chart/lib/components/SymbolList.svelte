<script>
  export let symbols;

  /**
   * @param {AssetSymbol} s
   */
  const onSymbolClicked = s => {};
</script>

<div>
  {#if symbols.length}
    <h2 class="py-5 text-center font-bold pointer-events-none select-none">Symbols</h2>

    <div>
      {#each symbols as symbol}
        <button on:click={() => onSymbolClicked(symbol)} class="block">
          <span class="px-5 hover:bg-gray-200 select-none">{symbol.name}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>
