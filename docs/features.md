# Features

## Flows - A Rigurous Definition

A *flow* in this context is a directed, usually but not necessarily acyclic, multigraph whose vertices are *nodes* with *connections* as edges to other nodes.

The fundamental operations to perform on a flow are

- adding a node
- removing a node and all incident connections
- adding a connection between ports of two different nodes
- removing an existing connection

### Flow Modes

### data flows

The default flow mode is *data*. The flow execution here is defined as follows:

By calling `Node.set_output_val(index, val)`, every outgoing connection is *activated*, with `val` as payload, which leads to an *update event* in every connected node. No automatic inspection, nor modification is performed on `val`. If there are multiple connections, the order of activation is the order in which they have been added.

### exec flows

> [!NOTE]
> While the *data* mode is the more common use case, you can think of the *exec* mode as UnrealEngine's BluePrints (*exec*) compared to their material editor (*data*). The *exec* mode implementation might receive some modifications in the future.

<!-- There are two types of connections, namely *data* and *exec* connections, and hence, two types of node ports. Usually you will want to only use data connections and ports (-> *data flows*).  -->

For exec connections, by calling `Node.exec_output(index)`, the same effects take place as for data propagation described above, just that there is no `val` payload, it's just an activation signal causing an update.

The fundamental difference is that in contrast to *data* mode, data is not forward propagated on change, but requested backwards, meaning a combinational node passively generating some data (like an addition on two values at inputs) not updated when input data changes, but when the output is requested in another connected node via `Node.input(index)`. See the Ryven documentation for an example.

***

The mode of a flow (*data* or *exec*) can be set at any time using `Flow.set_algorithm_mode`, default is *data*.

In both cases the `inp` parameter in `Node.update_event` represents the input index that received data or a signal respectively.

## Nodes System

Nodes are subclasses of the `Node` class. Single node instances are instances of their class, and the basic properties that apply on all those nodes equally are stored as static attributes. Individually changing properties include inputs and outputs (which can be added, removed and modified at any time), display title, actions (see below) etc. You can put any code into your node classes, no limitations, and for sophisticated usage you can override the default behavior by reimplementing methods and creating your own `NodeBase` class(es).

<!--
One very important feature is the possibility of defining custom GUI components, i.e. widgets, for your nodes. A node can have a `main_widget` and input widgets, whose classes are stored in the `input_widget_classes` attribute.
-->

### Special Actions

Special actions are a very simple way to define right click operations for your nodes. The non-static `Node.special_actions` attribute is a dictionary which you can edit like this

```python
# creating a new entry
self.actions['add some input'] = {'method': self.add_some_input_action}


# with a corresponding method
def add_some_input_action(self):
    self.create_input(label='new input', type_='data')


# removing an entry
del self.actions['add some input']

# storing individual data for multiple actions pointing to the same target method
# which enables dynamic, current state dependent actions
self.actions['add some input at index 0'] = {
    'method': self.add_some_input_at,
    'data': 0
}
self.actions['add some input at index 1'] = {
    'method': self.add_some_input_at,
    'data': 1
}


def add_some_input_at(self, index):
    self.create_input(label='inserted input', type_='data')
```

Special actions are saved and reloaded automatically.

> [!WARNING]
> Only refer to your according node's methods in the `method` field, not some other objects'. When saving, the referred method's name is stored and the method field in the `special_actions` entry is recreated on load via `getattr(node, method_name)`.

### Custom GUI

You can add custom Qt widgets to your nodes. For instructions on how to register custom widgets in your nodes see Ryven docs.

## Load&Save

To save a project use `Session.serialize()`. To load a saved project use `Session.load()`. Before loading a project, you need to register all required nodes in the session.

## Script Variables

Script variables are a nice way to improve the interface to your data. There is a really simple but extremely powerful *registration system* that you can use to register methods as *receivers* on a variable name with a method that gets called every time a script var's value with that name changed. The registration process is part of the API of the `Node` class, so you can easily create highly dynamic nodes.

> EXAMPLE
>
> I made a small *Matrix* node in Ryven where you can just type a few numbers into a small textedit (which is the custom `main_widget` of the node) and it creates a numpy array out of them. But you can also type in the name of a script variable somewhere (instead of a number) which makes the matrix node register as a receiver, so it updates and regenerates the matrix every time the value of a script variable with that name updated.
    
> [!NOTE]
> You could also work with default variables, for example, that you always create when creating a new script, by default, which all your nodes use to communicate or transmit data in more complex ways. This illustrates, there is really a bunch of quite interesting possibilities for sophisticated optimization with this. The system might be expanded in the future.

## Logging

Every *script* has a *logs manager*. You can use [API](../api/#class-logger) to write messages to default loggers and to request custom loggers (`python.logging.Logger`) and write directly to them. The `Node`'s API already includes methods for requesting custom loggers.

<!--
## Convenience Classes

ryvecore already comes with a few convenience classes for widgets. Those convenience classes only use ryvencore's public API, so if you have experience with Qt, you can totally implemenent them yourself. But in most cases they make it much easier to get started. See [convenience GUI section](../conv_gui).
-->

## Styling

Of course, design splays a huge role when talking about *visual* scripting. Therefore, there's a focus on styling freedom.

### Flow Themes

There is a list of available flow themes (which will hopefully grow). You can choose one via `Session.design.set_flow_theme()`. Currently available flow themes are

- `pure dark`
- `pure light`
- `colorful dark`
- `colorful light`
- `Ueli`
- `Blender`
- `Simple`
- `Toy`
-`Tron`

To make sure you can create a look that fits in nicely wherever you might integrate your editor, you can customize the colors for all the above themes using a config json file and passing it to the design using `Session.design.load_from_config(filepath)`. The json file should look like this, for any value you can either write `"default"` or specify a specific setting according to the instructions in the info box.

<details><summary>config file</summary>


You can also specify the initial flow theme, the performance mode (`'pretty'` or `'fast'`) and animations (which currently don't work I think). You can just copy the following json, save it in a file and specify.
```python
{
  "init flow theme": "pure light",
  "init performance mode": "pretty",
  "init animations enabled": true,
  "flow themes": {
    "Toy": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default"
    },
    "Tron": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default"
    },
    "Ghost": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "nodes color": "default",
      "small nodes color": "default"
    },
    "Blender": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "nodes color": "default"
    },
    "Simple": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "nodes background color": "default",
      "small nodes background color": "default"
    },
    "Ueli": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "nodes background color": "default",
      "small nodes background color": "default"
    },
    "pure dark": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "extended node background color": "default",
      "small node background color": "default",
      "node title color": "default",
      "port pin pen color": "default"
    },
    "pure light": {
      "exec connection color": "default",
      "exec connection width": "default",
      "exec connection pen style": "default",
      "data connection color": "default",
      "data connection width": "default",
      "data connection pen style": "default",
      "flow background color": "default",

      "extended node background color": "default",
      "small node background color": "default",
      "node title color": "default",
      "port pin pen color": "default"
    }
  }
}
```

</details>

Also note that the syntax of these configurations might receive some changes in the future. Give non-default values for widths in number format, not `str`. Possible values for pen styles are

- `solid line`
- `dash line`
- `dash dot line`
- `dash dot dot line`
- `dot line`

Give colors as string in hex format (also compatible with alpha values like `#aabb4499`).

### StyleSheets

The styling of widgets is pretty much in your hands. 
<!-- You can also store a stylesheet via `Session.design.set_stylesheet()` which is then accessible in custom node widget classes via `self.session.design.global_stylesheet`.  -->
When making a larger editor, you can style the builtin widgets (like the builtin input widgets for nodes) by referencing their class names in your qss.

## Class Customizations

There is currently a (*very* alpha) option to provide your own reimplementations for internally defined classes to add functionality to your editor.

> [!WARNING]
> This system is most likely going to change a few times. Also be aware that future changes on those internal parts will most likely frequently break your code. The goal is to get an internal system running solid enough to not receive frequent changes anymore.

There are no detailed instructions on that in the docs yet, but you can take a look at the implementations, and then pass your reimplementations of the classes you want to enhance to the `CLASSES` dict, **before** initializing a `Session`.

<!-- ## Customizing Connections

You can provide your own reimplementations of the connection classes, since this is an excellent point to add domain-specific additional functionality to your editor (like 'edge weights' for example).  -->

## Flow View Features

The `FlowView` class, which is a subclass of `QGraphicsView`, supports some special features such as

- stylus support for adding simple handwritten notes
- rendered images of the flow including high res for presentations

## Threading

The internal communication between backend (`ryvencore`) and frontend (`ryvencore-qt`) is done in a somewhat thread-safe way. This means, you can initialize the `Session` object in a separate thread, and provide a GUI parent for the `FlowView` which will then be initialized in this GUI component's thread. Of course, Python is very limited for threading due to the GIL. However, threading your components still improves concurrency, i.e. your session is not significantly slown down by the frontend. Further parallelization of the tasks that your individual nodes perform is up to you.

## GUI-less Deployment

You can deploy saved projects (`Session.serialize()`) directly on `ryvencore` without any frontend dependencies. You have full access to the whole `ryvencore` API, so you can even perform all modifications with the expected results. GUI-less deployment is like code generation but better, since you still have API access and `ryvencore` is lightweight.

```python
if __name__ == '__main__':

    with open('path/to/your/project_file', 'r') as f:
        project_str = f.read()

    project_dict = json.loads(project_str)

    # creating session and loading the contents
    session = Session(no_gui=True)
    session.register_nodes([ <your_used_nodes_here> ])
    scripts = session.load(project_dict)

    # now you have manual access like this...
    myscript = scripts[0]
    myflow = script.flow

    node1, node2, node3 = flow.nodes
    node1.update()
```

Which of the API calls you use in `ryvencore-qt` don't come from `ryvencore` is indicated in the API reference (basically everything frontend/widgets-related). Of course, your nodes are not allowed to access `ryvencore-qt` API, as this API does not exist when running it on the backend, since there is no frontend then. To make your nodes compatible with this, you can check the boolean `Session.gui` attribute to determine whether the session is aware of a frontend or not.

``` python
def update_event(self, inp=-1):

    # doing some work
    
    if self.session.gui:
        self.main_widget().update()
    
    # some more work
```
