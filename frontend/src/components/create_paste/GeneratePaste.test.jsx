import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import GeneratePaste from "./GeneratePaste";
import { createPaste } from "../../api";

// Mock the API module the component talks to.
vi.mock("../../api", () => ({
  createPaste: vi.fn(),
}));

describe("GeneratePaste", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the form initially", () => {
    render(<GeneratePaste />);

    expect(screen.getByText("PasteBin")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText(/paste code snippets here/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /generate link/i })
    ).toBeInTheDocument();
  });

  it("shows an error and does not call the API when submitting empty content", async () => {
    const user = userEvent.setup();
    render(<GeneratePaste />);

    await user.click(screen.getByRole("button", { name: /generate link/i }));

    expect(screen.getByText("Content cannot be empty")).toBeInTheDocument();
    expect(createPaste).not.toHaveBeenCalled();
  });

  it("shows an error when submitting whitespace-only content", async () => {
    const user = userEvent.setup();
    render(<GeneratePaste />);

    await user.type(
      screen.getByPlaceholderText(/paste code snippets here/i),
      "   "
    );
    await user.click(screen.getByRole("button", { name: /generate link/i }));

    expect(screen.getByText("Content cannot be empty")).toBeInTheDocument();
    expect(createPaste).not.toHaveBeenCalled();
  });

  it("submits content, calls the API, and shows the created paste URL", async () => {
    const user = userEvent.setup();
    createPaste.mockResolvedValueOnce({ id: "abc123" });

    render(<GeneratePaste />);

    await user.type(
      screen.getByPlaceholderText(/paste code snippets here/i),
      "console.log('hi')"
    );
    await user.click(screen.getByRole("button", { name: /generate link/i }));

    await waitFor(() => {
      expect(createPaste).toHaveBeenCalledWith("console.log('hi')");
    });

    const expectedUrl = `${window.location.origin}/abc123`;
    expect(await screen.findByText(expectedUrl)).toBeInTheDocument();
    expect(screen.getByText("Success!")).toBeInTheDocument();
  });

  it("shows a loading state while the request is in flight", async () => {
    const user = userEvent.setup();
    let resolvePromise;
    createPaste.mockReturnValueOnce(
      new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    render(<GeneratePaste />);

    await user.type(
      screen.getByPlaceholderText(/paste code snippets here/i),
      "some code"
    );
    await user.click(screen.getByRole("button", { name: /generate link/i }));

    expect(
      screen.getByRole("button", { name: /generating/i })
    ).toBeDisabled();

    resolvePromise({ id: "xyz789" });

    await waitFor(() => {
      expect(
        screen.queryByRole("button", { name: /generating/i })
      ).not.toBeInTheDocument();
    });
  });

  it("shows an error message when the API call fails", async () => {
    const user = userEvent.setup();
    createPaste.mockRejectedValueOnce(new Error("Network error"));

    render(<GeneratePaste />);

    await user.type(
      screen.getByPlaceholderText(/paste code snippets here/i),
      "some code"
    );
    await user.click(screen.getByRole("button", { name: /generate link/i }));

    expect(await screen.findByText("Network error")).toBeInTheDocument();
    // Should stay on the form, not switch to the "created" view.
    expect(
      screen.getByPlaceholderText(/paste code snippets here/i)
    ).toBeInTheDocument();
  });

  describe("copy to clipboard", () => {
    afterEach(() => {
      vi.restoreAllMocks();
    });

    it("copies the paste URL and shows 'Copied!' feedback", async () => {
      const user = userEvent.setup();
      const writeTextSpy = vi
        .spyOn(navigator.clipboard, "writeText")
        .mockResolvedValueOnce(undefined);
      createPaste.mockResolvedValueOnce({ id: "copy-me" });

      render(<GeneratePaste />);

      await user.type(
        screen.getByPlaceholderText(/paste code snippets here/i),
        "some code"
      );
      await user.click(screen.getByRole("button", { name: /generate link/i }));

      const copyButton = await screen.findByRole("button", {
        name: /copy to clipboard/i,
      });
      await user.click(copyButton);

      const expectedUrl = `${window.location.origin}/copy-me`;
      expect(writeTextSpy).toHaveBeenCalledWith(expectedUrl);
      expect(
        await screen.findByRole("button", { name: /^copied!$/i })
      ).toBeInTheDocument();
    });

    it("shows a copy error if the clipboard write fails", async () => {
      const user = userEvent.setup();
      vi.spyOn(navigator.clipboard, "writeText").mockRejectedValueOnce(
        new Error("denied")
      );
      createPaste.mockResolvedValueOnce({ id: "fail-copy" });

      render(<GeneratePaste />);

      await user.type(
        screen.getByPlaceholderText(/paste code snippets here/i),
        "some code"
      );
      await user.click(screen.getByRole("button", { name: /generate link/i }));

      const copyButton = await screen.findByRole("button", {
        name: /copy to clipboard/i,
      });
      await user.click(copyButton);

      expect(
        await screen.findByText("Failed to copy link.")
      ).toBeInTheDocument();
    });
  });
});
