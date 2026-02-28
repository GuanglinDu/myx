<script setup lang="ts">
</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

    <div class="main-left col-span-1">
      <!-- Person 1 -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-1">
            <img
              src="@/assets/Brian-40x40px.png"
              alt="avatar"
              class="w-[40px] rounded-full"
            />
            
            <p class="tet-xs">Code With Guanglin</p>
          </div>

          <span class="text-xs text-gray-500">18 minutes ago</span>
        </div>

        <!-- Person 2 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-1">
            <img
              src="@/assets/Brian-40x40px.png"
              alt="avatar"
              class="w-[40px] rounded-full"
            />
            
            <p class="tet-xs">Code With Guanglin</p>
          </div>

          <span class="text-xs text-gray-500">18 minutes ago</span>
        </div>
      
        <!-- Person 3 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-1">
            <img
              src="@/assets/Brian-40x40px.png"
              alt="avatar"
              class="w-[40px] rounded-full"
            />
            
            <p class="tet-xs">Code With Guanglin</p>
          </div>

          <span class="text-xs text-gray-500">18 minutes ago</span>
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <!-- The existing posts -->
      <div class="bg-white border border-gray-200 rounded-lg">
        
        <!-- Post 1 on the right side -->
        <div class="flex flex-row space justify-end p-4">
          <div calss="flex mt-2 space-x-3 max-w-md ml-auto justify-end">
            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
              <p class="text-sm">
                Trust your hard work. It's unlocking doors you can't see yet.
              </p>
            </div>
            <span class="text-xs text-gray-500 leading-none">15 min ago</span>
          </div>
          <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
            <img
              src="@/assets/Brian-40x40px.png"
              class="w-[40px] rounded-full"
            />
          </div>
        </div>

        <!-- Post 2 on the right side -->
        <div class="flex flex-row space justify-end p-4">
          <div calss="flex mt-2 space-x-3 max-w-md ml-auto justify-end">
            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
              <p class="text-sm">
                Slow progress is better than no progress. Stay positive and don't give up.
              </p>
            </div>
            <span class="text-xs text-gray-500 leading-none">12 min ago</span>
          </div>
          <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
            <img
              src="@/assets/Brian-40x40px.png"
              class="w-[40px] rounded-full"
            />
          </div>
        </div>

        <!-- Post 1 on the left side -->
        <div class="flex flex-row space justify-start p-4">
          <div class="flex-shrink-0 h-10 w-10 rounded-full">
            <img
              src="@/assets/Adrian-40x40px.png"
              class="w-[40px] rounded-full"
            />
          </div>
          <div calss="flex mt-2 space-x-3 max-w-md ml-auto">
            <div class="bg-gray-300 text-black p-3 rounded-l-lg rounded-br-lg">
              <p class="text-sm">
                It's time to forgive yourself for making mistakes when you were doing your best to survive.
              </p>
            </div>
            <span class="text-xs text-gray-500 leading-none">8 min ago</span>
          </div>
        </div>

        <!-- Post 2 on the left side -->
        <div class="flex flex-row space justify-start p-4">
          <div class="flex-shrink-0 h-10 w-10 rounded-full">
            <img
              src="@/assets/Adrian-40x40px.png"
              class="w-[40px] rounded-full"
            />
          </div>
          <div calss="flex mt-2 space-x-3 max-w-md ml-auto">
            <div class="bg-gray-300 text-black p-3 rounded-l-lg rounded-br-lg">
              <p class="text-sm">
                No matter how good you are, how nice you are, how kind you are, or how caring you are, if you are in the wrong place, you're never valued and apprecicated.
              </p>
            </div>
            <span class="text-xs text-gray-500 leading-none">8 min ago</span>
          </div>
        </div>
      </div>

      <!-- The text area to create textual posts -->
      <div class="bg-white border border-gray-200 rounded-lg">
        <!-- (2.1.1/3) The textarea element -->
        <div class="p-4">
          <textarea
            class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="What do you want to say?"
          />
        </div>

        <!-- The Post button -->
        <div class="p-4 border-t border-gray-100 flex justify-between">
          <a href="#"
             class="inline-block py-4 px-6 bg-purple-600 text-white
                    rounded-lg">
            Post
          </a>
        </div>
      </div>
   </div>
  </div>
</template>
