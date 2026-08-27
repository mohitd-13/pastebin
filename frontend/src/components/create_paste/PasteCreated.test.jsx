import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import PasteCreated from "./PasteCreated";

describe("PasteCreated", () => {
  it("renders the paste URL", () => {
    render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={vi.fn()}
        error=""
        copyError=""
      />
    );

    expect(screen.getByText("http://localhost:3000/abc123")).toBeInTheDocument();
  });

  it("shows 'Copy to Clipboard' by default and 'Copied!' when copied is true", () => {
    const { rerender } = render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={vi.fn()}
        error=""
        copyError=""
      />
    );

    expect(
      screen.getByRole("button", { name: /copy to clipboard/i })
    ).toBeInTheDocument();

    rerender(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={true}
        copyToClipboard={vi.fn()}
        error=""
        copyError=""
      />
    );

    expect(screen.getByRole("button", { name: /^copied!$/i })).toBeInTheDocument();
  });

  it("calls copyToClipboard when the button is clicked", async () => {
    const user = userEvent.setup();
    const copyToClipboard = vi.fn();

    render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={copyToClipboard}
        error=""
        copyError=""
      />
    );

    await user.click(screen.getByRole("button", { name: /copy to clipboard/i }));

    expect(copyToClipboard).toHaveBeenCalledTimes(1);
  });

  it("renders an error message when error is provided", () => {
    render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={vi.fn()}
        error="Something went wrong"
        copyError=""
      />
    );

    expect(screen.getByText("Something went wrong")).toBeInTheDocument();
  });

  it("renders a copyError message when copyError is provided", () => {
    render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={vi.fn()}
        error=""
        copyError="Failed to copy link."
      />
    );

    expect(screen.getByText("Failed to copy link.")).toBeInTheDocument();
  });

  it("renders neither message when there are no errors", () => {
    render(
      <PasteCreated
        pasteUrl="http://localhost:3000/abc123"
        copied={false}
        copyToClipboard={vi.fn()}
        error=""
        copyError=""
      />
    );

    expect(screen.queryByText(/failed to copy/i)).not.toBeInTheDocument();
  });
});
