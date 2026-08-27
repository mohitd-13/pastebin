import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import PasteForm from "./PasteForm";

describe("PasteForm", () => {
  it("renders the textarea and submit button", () => {
    render(
      <PasteForm
        content=""
        onContentChange={vi.fn()}
        loading={false}
        submitHandler={vi.fn()}
        error=""
      />
    );

    expect(
      screen.getByPlaceholderText(/paste code snippets here/i)
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /generate link/i })
    ).toBeInTheDocument();
  });

  it("displays the current content value", () => {
    render(
      <PasteForm
        content="hello world"
        onContentChange={vi.fn()}
        loading={false}
        submitHandler={vi.fn()}
        error=""
      />
    );

    expect(screen.getByPlaceholderText(/paste code snippets here/i)).toHaveValue(
      "hello world"
    );
  });

  it("calls onContentChange as the user types", async () => {
    const user = userEvent.setup();
    const onContentChange = vi.fn();

    render(
      <PasteForm
        content=""
        onContentChange={onContentChange}
        loading={false}
        submitHandler={vi.fn()}
        error=""
      />
    );

    await user.type(screen.getByPlaceholderText(/paste code snippets here/i), "hi");

    // called once per keystroke
    expect(onContentChange).toHaveBeenCalledTimes(2);
    expect(onContentChange).toHaveBeenNthCalledWith(1, "h");
    expect(onContentChange).toHaveBeenNthCalledWith(2, "i");
  });

  it("calls submitHandler when the form is submitted", async () => {
    const user = userEvent.setup();
    const submitHandler = vi.fn((e) => e.preventDefault());

    render(
      <PasteForm
        content="some content"
        onContentChange={vi.fn()}
        loading={false}
        submitHandler={submitHandler}
        error=""
      />
    );

    await user.click(screen.getByRole("button", { name: /generate link/i }));

    expect(submitHandler).toHaveBeenCalledTimes(1);
  });

  it("disables the textarea and button, and shows 'Generating...' while loading", () => {
    render(
      <PasteForm
        content=""
        onContentChange={vi.fn()}
        loading={true}
        submitHandler={vi.fn()}
        error=""
      />
    );

    expect(screen.getByPlaceholderText(/paste code snippets here/i)).toBeDisabled();
    const button = screen.getByRole("button", { name: /generating/i });
    expect(button).toBeInTheDocument();
    expect(button).toBeDisabled();
  });

  it("renders an error message when error is provided", () => {
    render(
      <PasteForm
        content=""
        onContentChange={vi.fn()}
        loading={false}
        submitHandler={vi.fn()}
        error="Content cannot be empty"
      />
    );

    expect(screen.getByText("Content cannot be empty")).toBeInTheDocument();
  });

  it("does not render an error message when error is empty", () => {
    render(
      <PasteForm
        content=""
        onContentChange={vi.fn()}
        loading={false}
        submitHandler={vi.fn()}
        error=""
      />
    );

    expect(screen.queryByText(/content cannot be empty/i)).not.toBeInTheDocument();
  });
});
