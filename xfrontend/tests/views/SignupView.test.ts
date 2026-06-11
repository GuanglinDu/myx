import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import SignupView from "@/views/SignupView.vue";
import { setActivePinia, createPinia } from "pinia";
import { createApp } from "vue";

// Mock axios. Read the Q&A from Claude Code below.
vi.mock("axios", () => ({
  default: {
    post: vi.fn().mockResolvedValue({ data: { message: "success" } }),
    get: vi.fn(),
    defaults: { headers: { common: {} } },
  },
}));

describe("SignupView", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it("renders signup form correctly", () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    expect(wrapper.find("h1").text()).toBe("Sign up");
    expect(wrapper.find('input[name="name"]').exists()).toBe(true);
    expect(wrapper.find('input[name="email"]').exists()).toBe(true);
    expect(wrapper.find('input[name="password1"]').exists()).toBe(true);
    expect(wrapper.find('input[name="password2"]').exists()).toBe(true);
    expect(wrapper.find("button").text()).toBe("Sign up");
  });

  it("has link to login page", () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    expect(wrapper.html()).toContain("Already have an account");
  });

  it("form fields are interactive", async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    const nameInput = wrapper.find('input[name="name"]');
    await nameInput.setValue("Test User");
    expect((nameInput.element as HTMLInputElement).value).toBe("Test User");

    const emailInput = wrapper.find('input[name="email"]');
    await emailInput.setValue("test@example.com");
    expect((emailInput.element as HTMLInputElement).value).toBe(
      "test@example.com",
    );
  });

  it("calls toastStore.showToast when name is missing", async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    // Fill other fields but not name
    await wrapper.find('input[name="email"]').setValue("test@example.com");
    await wrapper.find('input[name="password1"]').setValue("password123");
    await wrapper.find('input[name="password2"]').setValue("password123");

    // Spy on showToast
    const toastStoreModule = await import("@/stores/toast");
    const showToastSpy = vi.spyOn(
      toastStoreModule.useToastStore(),
      "showToast",
    );

    await wrapper.find("form").trigger("submit.prevent");

    // Verify showToast was called with expected args
    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      "Your name is missing",
      "bg-red-300",
    );
  });

  it("calls toastStore.showToast when passwords do not match", async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    await wrapper.find('input[name="name"]').setValue("Test User");
    await wrapper.find('input[name="email"]').setValue("test@example.com");
    await wrapper.find('input[name="password1"]').setValue("password123");
    await wrapper.find('input[name="password2"]').setValue("differentpassword");

    const toastStoreModule = await import("@/stores/toast");
    const showToastSpy = vi.spyOn(
      toastStoreModule.useToastStore(),
      "showToast",
    );

    await wrapper.find("form").trigger("submit.prevent");

    expect(showToastSpy).toHaveBeenCalledWith(
      5000,
      "The password does not match",
      "bg-red-300",
    );
  });

  it("submits form to API when all fields are valid", async () => {
    const wrapper = mount(SignupView, {
      global: {
        stubs: {
          RouterLink: { template: "<a><slot /></a>" },
        },
      },
    });

    await wrapper.find('input[name="name"]').setValue("Test User");
    await wrapper.find('input[name="email"]').setValue("test@example.com");
    await wrapper.find('input[name="password1"]').setValue("password123");
    await wrapper.find('input[name="password2"]').setValue("password123");
    await wrapper.find("form").trigger("submit.prevent");

    // Wait for the async axios call
    await new Promise((resolve) => setTimeout(resolve, 50));

    // Verify API was called
    const axios = await import("axios");
    expect(axios.default.post).toHaveBeenCalled();
    expect(axios.default.post).toHaveBeenCalledWith(
      "/api/signup/",
      expect.any(Object),
    );
  });
});

/** Appended at 11:16:40 on 20260611 Thu by Guanglin Du.

What does vi do in SinupVie.test.ts? (Ask Claude Code)

  Thought for 34s, read 1 file, listed 1 directory

vi is the Vitest testing utility object — Vitest's equivalent of Jest's jest. It's imported from vitest (line 1) and gives you mock/spy helpers for isolating the unit under test. In SignupView.test.ts it's used in four distinct ways:

1. vi.mock(...) — module-level auto-mock (lines 8-14)

vi.mock("axios", () => ({
  default: {
    post: vi.fn().mockResolvedValue({ data: { message: "success" } }),
    get: vi.fn(),
    defaults: { headers: { common: {} } },
  },
}));

vi.mock is hoisted by Vitest's transformer to the top of the file, before any imports run. When SignupView.vue does import axios from 'axios', it gets this stub instead of the real axios, so no network calls ever leave the test process. The factory function returns the replacement module — here, a default export with a post mock that resolves to a fake "success" response.

2. vi.fn() — creates a spy/mock function (lines 10-11)

post: vi.fn().mockResolvedValue({ data: { message: "success" } }),
get: vi.fn(),

vi.fn() returns a callable mock that records every invocation. You can:
- Assert what it was called with (line 152: expect(axios.default.post).toHaveBeenCalledWith("/api/signup/", expect.any(Object))).
- Pre-program return values with .mockResolvedValue(...) (returns a Promise that resolves) or .mockReturnValue(...) (synchronous).
- Clear/reset between tests with mockReset().

In this file, the post mock is set up once at module level and reused across all tests — that's why the "submits form" test on line 131 can import axios and just check toHaveBeenCalled() without re-configuring the mock.

3. vi.clearAllMocks() — resets mock state (line 19)

beforeEach(() => {
  setActivePinia(createPinia());
  vi.clearAllMocks();
});

Wipes the call history of every mock fn so each test starts clean. Without this, the second test would see the calls the first test made.

4. vi.spyOn(...) — wraps an existing method (lines 87-90, 117-120)

const toastStoreModule = await import("@/stores/toast");
const showToastSpy = vi.spyOn(
  toastStoreModule.useToastStore(),
  "showToast",
);

vi.spyOn is different from vi.fn(): instead of replacing a function, it wraps the real one so it still runs, but Vitest tracks the calls. Here the test wants the real showToast to run (so it can verify toast behavior) but also wants to assert that it was called with specific arguments. If you also want to override the behavior, chain .mockImplementation(...) on the spy.

spyOn is per-test, which is why it's created inside each it() block rather than at module scope like vi.mock.

---
Quick mental model

┌─────────────────────────┬───────────────────────────┬─────────────────────────────────────────────────┐
│         Helper          │     What it replaces      │                    Use case                     │
├─────────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ vi.mock(path, factory)  │ An entire module          │ Stop SignupView.vue from making real HTTP calls │
├─────────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ vi.fn()                 │ A function you control    │ Pre-program return values, count calls          │
├─────────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ vi.spyOn(obj, 'method') │ A method on a real object │ Observe how the SUT calls into its dependencies │
├─────────────────────────┼───────────────────────────┼─────────────────────────────────────────────────┤
│ vi.clearAllMocks()      │ Nothing — resets state    │ Test isolation in beforeEach                    │
└─────────────────────────┴───────────────────────────┴─────────────────────────────────────────────────┘

For the test runner mechanics ("how does hoisting work? what runs first?"), the Vitest docs page on mocking modules (https://vitest.dev/guide/mocking.html) is the canonical reference. The two gotchas worth knowing:

- vi.mock calls are hoisted — they run before imports. Don't reference variables from the test file's outer scope inside the factory unless you prefix with vi.hoisted(...).
- vi.spyOn requires the spied object to be a real one you can call. That's why the toast tests do await import("@/stores/toast") and call useToastStore() inside the test — the spy needs the real store instance returned by the real factory.

What is an SUT call in Vue.js? - Google AI Overview

In Vue.js testing, an SUT (System Under Test) is simply the specific Vue component or composable you are actively testing. It defines the boundaries of your test, isolating the component from its external dependencies (like Vuex, Pinia, or API endpoints).
*/
