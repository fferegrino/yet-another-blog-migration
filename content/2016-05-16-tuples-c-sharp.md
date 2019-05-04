layout: post
title: "Tuples en C#"
date: 2016-05-16 19:00:01
author: Antonio Feregrino
excerpt: Seguramente te ha pasado, alguna vez has pensado &quot;Ojalá pudiera devolver dos cosas desde este método&quot; y si bien recuerdas que los métodos en C# únicamente pueden tener un solo tipo de retorno, es posible devolver más de dos valores haciendo uso de la clase genérica Tuple.
featured_image: tuples.png
images_folder: /aprende-c-sharp/
github: https://github.com/ThatCSharpGuy/aprende-c-sharp/tree/master/Tuples
tweet_id: 732374334027628544
lang: es
tags: AprendeCSharp
featured_tag: AprendeCSharp

Seguramente te ha pasado, alguna vez has pensado "Ojalá pudiera devolver dos cosas desde este método" y si bien recuerdas que los <a href="../metodos-c-sharp">métodos en C#</a> únicamente pueden tener un solo tipo de retorno, es posible devolver más de dos valores haciendo uso de la clase genérica `Tuple`.  

Podemos ver a `Tuple` (o tupla) como un auxiliar para el programador, que **permite "agrupar" otros tipos dato dentro de uno solo**, para así tratarlos como uno solo, esto, a través de varias clases genéricas definidas de la siguiente manera:  

 - `Tuple<T1>`
 - `Tuple<T1, T2>`
 - `Tuple<T1, T2, T3>`
 - `Tuple<T1, T2, T3, T4>`
 - `Tuple<T1, T2, T3, T4, T5>`
 - `Tuple<T1, T2, T3, T4, T5, T6>`
 - `Tuple<T1, T2, T3, T4, T5, T6, T7>`
 - `Tuple<T1, T2, T3, T4, T5, T6, T7, TRest>`
 
 ## Creando tuplas
 
A través de los tipos `T#` se define el contenido de la clase, siendo así que para crear una tupla que contiene un entero y dos cadenas debemos usar:  

{% highlight csharp %}
var t = new Tuple<int, string, string>(1, "A", "B");
{% endhighlight %}

O, por ejemplo, si quisiéramos crear algo más complejo como una clase que contiene un entero, un decimal, un objeto, otro entero, un booleano y un flotante, tendríamos que hacer algo como esto:    

{% highlight csharp %}
var t1 = new Tuple<int, decimal, object, int, bool, float>(3, 1.5m, new { emoji = ":grin:" }, 5, true, 7.5f);
{% endhighlight %}

Uhhmm, la sintaxis se pone un poco complicada, ¿no? para eliminar esta sintaxis complicada, podemos usar el método estático `Create` de la clase `Tuple` para crear tuplas:  

{% highlight csharp %}
var t1 = Tuple.Create(3, 1.5m, new { emoji = ":grin:" }, 5, true, 7.5f);
{% endhighlight %}

Este método, inferirá de los tipos de dato a partir de los parámetros pasados como argumentos.

## Accediendo a los miembros
Una vez creada la clase (ya sea con el constructor o el método estático), podemos acceder a cada uno de los datos a través de las propiedades llamadas  `Item#`, donde # es el número de la propiedad a la que nos referimos:  

{% highlight csharp %}
Console.WriteLine(t.Item1); // 1 -> int
Console.WriteLine(t.Item2 + " - " + t.Item3 ); // "A - B" -> string
{% endhighlight %}

Es importante señalar que las propiedades de la clase `Tuple` son de solo lectura, y que una vez asignadas en el constructor, no pueden ser modificadas:  

{% highlight csharp %}
// t1.Item4 = 7; // Error, solo lectura
{% endhighlight %}

## Ejemplos de uso  

### Como parámetros de método
Podríamos pensar en un método como este: 
  
{% highlight csharp %}
string MegaMetodoArgumentos(int studentId, int classroomId, string type, decimal sum, bool active)
{% endhighlight %}

Para llamarlo necesitaríamos escribir algo como esto:  

{% highlight csharp %}
MegaMetodoArgumentos(10, 3, "MX", 3.1m, true);
{% endhighlight %}

O, también podríamos haber escrito el método de la siguiente manera:  

{% highlight csharp %}
string MegaMetodoTuple(Tuple<int, int, string, decimal, bool> args)
{% endhighlight %}

E invocarlo así:  

{% highlight csharp %}
var tuple = Tuple.Create(10, 3, "MX", 3.1m, true);
MegaMetodoTuple(tuple);  
{% endhighlight %}

### Como valores de retorno

El beneficio se nota más cuando se usa una tupa como valor de retorno, imaginemos un método en el que convertimos tomamos un color definido en hexadecimal y lo convertimos a su representación RGB en decimal.

Podríamos usar [parámetros de salida](http://thatcsharpguy.com/post/out-ref-c-sharp/):  

{% highlight csharp %}
private static void SplitColors(string hex, out int r, out int g, out int b)
{
    r = Int32.Parse(hex.Substring(0, 2), NumberStyles.HexNumber);
    g = Int32.Parse(hex.Substring(2, 2), NumberStyles.HexNumber);
    b = Int32.Parse(hex.Substring(4, 2), NumberStyles.HexNumber);
}
{% endhighlight %}

Pero también podríamos usar una tupla como valor de retorno:  

{% highlight csharp %}
private static Tuple<int, int, int> SplitColors(string hex)
{
    int r = Int32.Parse(hex.Substring(0, 2), NumberStyles.HexNumber);
    int g = Int32.Parse(hex.Substring(2, 2), NumberStyles.HexNumber);
    int b = Int32.Parse(hex.Substring(4, 2), NumberStyles.HexNumber);
    return Tuple.Create(r, g, b);
}
{% endhighlight %}

Entonces para llamarlo, simplemente necesitaríamos escribir lo siguiente:  

{% highlight csharp %}
string color = "3C8A3F";
var colors = SplitColors(color);
Console.WriteLine("{0} es R:{1} G:{2} B:{3}", color, colors.Item1, colors.Item2, colors.Item3);
{% endhighlight %}

## Tuplas de 8 elementos
Si volvemos a las definiciones de las clases `Tuple` puedes ver que existen hasta 8 versiones genéricas disponibles. Sin embargo, la octava una peculiaridad: el octavo valor no se almacena dentro de "Item8", sino dentro de otra tupla (a la que accedemos desde la propiedad `Rest`):  

{% highlight csharp %}
var megaTuple = Tuple.Create(1, 2, 3, 4, 5, 6, 7, 8);
//Console.WriteLine(miniTuple.Item8); // Item8 no existe, entonces tenemos que usar Rest:
Console.WriteLine(megaTuple.Rest.Item1); 
{% endhighlight %}

## Ejemplo de la vida real
Mmm... en realidad no existe alguna api dentro del framework de .NET que haga uso de tuplas, pero en específico se recomienda para:

 - Representar un set de datos, por ejemplo, un registro en una base de datos
 - Proveer acceso fácil, y manipulación de, un set de datos
 - Regresar múltiples valores de un método sin usar parámetros por referencia
 - Enviar múltiples valores a un método
 
## Lo que sigue
Revisa el <a href="https://github.com/ThatCSharpGuy/aprende-c-sharp/tree/master/Tuples" target="_blank" rel="nofollow">código que acompaña al post</a> y juegues un poco con él, sé que tal vez el asunto de los genéricos en C# puede causar un poco de confusión y es un tema que estoy planeando cubrir en un post futuro.
