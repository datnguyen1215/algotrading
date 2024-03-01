<script>
  import SquaresIcon from '$lib/components/Icons/Squares.svelte';
  import ChartIcon from '$lib/components/Icons/Chart.svelte';
  import PuzzleIcon from '$lib/components/Icons/Puzzle.svelte';
  import { page } from '$app/stores';

  let menus = [
    {
      name: 'Dashboard',
      url: '/',
      icon: SquaresIcon
    },
    {
      name: 'Chart',
      url: '/chart',
      icon: ChartIcon
    },
    {
      name: 'Strategies',
      url: '/strategies',
      icon: PuzzleIcon
    }
  ];
</script>

<ul>
  {#each menus as menu}
    <a href={menu.url}>
      <li
        class="flex items-center px-5 py-2 hover:bg-gray-200 cursor-pointer"
        class:active={$page.url.pathname == menu.url}
      >
        {#if menu.icon}
          <svelte:component this={menu.icon} class="w-5 h-5" />
        {/if}
        <span class="pl-2">{menu.name}</span>
      </li>
    </a>
  {/each}
</ul>

<style lang="postcss">
  .active {
    @apply bg-gray-200;
  }
</style>
