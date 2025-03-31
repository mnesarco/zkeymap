# Copyright (c) 2025 Frank David Martínez Muñoz <mnesarco>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

T = TypeVar("T")


def proxy(obj: T) -> T:
    """
    Returns a proxy object that wraps the given object.

    The returned proxy object is a :class:`Proxy` instance that forwards all
    attribute access, method calls and iteration to the wrapped object.

    The wrapped object can be changed at any time using the ``__itruediv__``
    operator. All references to the proxy object will see the new wrapped object.

    :param obj: The object to wrap.
    :return: A proxy object wrapping the given object.
    """
    return Proxy(obj)


class Proxy(Generic[T]):
    """
    A proxy object for a wrapped object.

    Allows to have a reference in scope while the actual wrapped object can be changed at any time.
    """

    _wrapped: T | None

    def __init__(self, obj: T | None) -> None:
        """
        Initialize a new proxy object.

        :param obj: The object to proxy or None to create an uninitialized proxy.
        """
        object.__setattr__(self, "_wrapped", obj)

    def __getattr__(self, name: str) -> Any:
        """Forwards attribute lookup to wrapped object."""
        return getattr(self._wrapped, name)

    def __setattr__(self, name: str, value: Any) -> Any:
        """Forwards attribute assignment to wrapped object."""
        setattr(self._wrapped, name, value)

    def __iter__(self) -> Iterator:
        """
        Forwards iteration to the wrapped object (if supported).

        :return: An iterator over the wrapped object.
        """
        return self._wrapped.__iter__()

    def __itruediv__(self, replace: T) -> T:  # noqa: PYI034, Proxy mimics T
        """
        Replace the wrapped object with the given one.

        :param replace: The object to become the new wrapped object.
        :return: The proxy object itself.
        """
        object.__setattr__(self, "_wrapped", replace)
        return self
