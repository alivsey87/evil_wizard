
# Defeat The Evil Wizard

---
---

### Welcome to my Defeat The Evil Wizard game!!

---
---

## TABLE OF CONTENTS

1. [App](#1-app)

2. [ProductList](#2-productlist)

3. [ProductItem](#3-productitem)

4. [CSS Styling](#4-css-styling)

---
---

## 1. App

The main parent component holding the state variable of products and renders the complete UI including the child [ProductList](#2-productlist) component, which is passed the `products` prop. The `originalProducts` array holds all of the product objects to be displayed, and the `products` state variable is set to this upon initiation. The `hasItems` state variable is used to check if the list is empty or not, which is needed in the `removeProduct()` and `restoreProduct()` functions. This is also used in conditionally rendering the "THERE ARE NO ITEMS!" message with "Restore List" button. Once `hasItems` is no longer truthy, the "Remove item" button is disabled, the "THERE ARE NO ITEMS!" `<p>` and "Restore list" `<button>` render:

```jsx
return (
    <>
      <h1>Welcome to Comp-Pheral</h1>
      <h2>Our Products:</h2>
      <ProductList products={products} />
      <button className='remove-button' onClick={removeProduct} disabled={!hasItems}>Remove item</button>
      {!hasItems && (
        <div>
          <p className='items-warning'>THERE ARE NO ITEMS!</p>
          <button className='restore-button' onClick={restoreProducts}>Restore list</button>
        </div>
      )}
    </>
  );
```  

---
---

## 2. ProductList

Child component of [App](#1-app) that receives the `products` prop that maps the products object array, passing each key as a prop to the [ProductItem](#3-productitem) child component:

```jsx
return products.map((product) => (
    <ProductItem
      id={product.id}
      name={product.name}
      price={product.price}
      description={product.description}
      image={product.image}
    />
  ));
```  

---
---

## 3. ProductItem

The final child component that renders the information passed down from the parent components. [App](#1-app) passes the `products` to [ProductList](#2-productlist), which is mapped and passed as props to this component. Each prop contains the value of the key from the product object and renders each to the appropriate html elements `<ul>`, `<li>` and `<img>`. The image conditionally renders when the state variable `showImage` is truthy, which occurs when the button displaying all the product info is clicked.

The meat-and-potatoes of this app thrives from this render:

```jsx
return (
    <>
      <button className="product-button" onClick={handleButtonClick}>
        <ul id={id} className="product">
          <li>{name}</li>
          <li>{price}</li>
          <li>{description}</li>
        </ul>
      </button>
      {showImage && (
        <div className="image-container">
          <img className="product-image" src={image} alt={`Photo of ${name}`} />
        </div>
      )}
    </>
  );
```  

---
---

## 4. CSS Styling

Since this is a "computer store" I decided to make the styling have a sort of ***machine*** kind of feel to it. I created linear gradients with grays and even added a cool "shine" effect when hovering over the product buttons. I achieved this (with a LOT of trial and error) by making the gradient background of the button in hover state actually larger than the button itself (seems there is a pseudo "overflow: hidden" here which was useful) and creating an animation that moved that background, giving the illusion that the reflected light was moving across:

```css
.product-button:hover {
    background: linear-gradient(45deg, rgba(65, 65, 65, 1.0), rgb(122, 122, 122), rgba(65, 65, 65, 1.0));
    background-size: 300%;
    cursor: pointer;
    transform: translateY(-2px);
    box-shadow: 2px 2px 5px rgb(32, 32, 32);
    animation: oohShiny 400ms 1 linear;
    animation-fill-mode: forwards;
}
```

```css
@keyframes oohShiny {
    0% {
        background-position: 0% 50%;
    }

    100% {
        background-position: 100% 50%;
    }
}
```

I created a lot of hover effects and smooth transitions to make a satisfying UI. Even making the images have a bit of animation and stop on hover. There are plenty of `box-shadow` usages to make the app pop and feel sort of tangible.

[back to top](#e-commerce-product-listing-app)
