import pygame


PgVector = pygame.math.Vector2


class World:
    def __init__(self, size, dt, gravity_acc):
        self.size = size
        self.dt = dt
        self.gravity_acc = PgVector(gravity_acc)


class CircleDrawer:
    def __init__(self, color, width):
        self.color = pygame.Color(color)
        self.width = width

    def __call__(self, screen, center, radius):
        pygame.draw.circle(screen, self.color, center, radius, self.width)


class LineDrawer:
    def __init__(self, color, width):
        self.color = pygame.Color(color)
        self.width = width

    def __call__(self, screen, pos1, pos2):
        for k in range(1,11):
            pygame.draw.circle(screen, self.color, pos1 + (pos2 - pos1)/11 * k, 1, self.width)


def compute_gravity_force(mass, gravity_acc):
    return mass * gravity_acc


def compute_viscous_damping_force(viscous_damping, vel):
    return -viscous_damping * vel


def integrate_symplectic(pos, vel, force, mass, dt):
    vel_new = vel + force / mass * dt
    pos_new = pos + vel_new * dt
    return pos_new, vel_new


class PointMass:
    def __init__(self, pos, vel, world, radius=10, mass=10,
                 viscous_damping=0.01, restitution=0.95, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer

        self.pos = PgVector(pos)
        self.vel = PgVector(vel)
        self.radius = radius
        self.mass = mass
        self.viscous_damping = viscous_damping
        self.restitution = restitution

        self.total_force = PgVector((0, 0))
        self.message_list = []

    def update(self):
        self.generate_force()
        self.move()
        self.total_force = PgVector((0, 0))
        self.message_list.clear()

    def draw(self, screen):
        self.drawer(screen, self.pos, self.radius)

    def receive_force(self, force):
        self.total_force += PgVector(force)

    def receive_message(self, msg):
        self.message_list.append(msg)

    def generate_force(self):
        force_g = compute_gravity_force(self.mass, self.world.gravity_acc)
        force_v = compute_viscous_damping_force(self.viscous_damping, self.vel)
        self.receive_force(force_g + force_v)

    def move(self):
        self.pos, self.vel = \
            integrate_symplectic(self.pos, self.vel, self.total_force, self.mass, self.world.dt)

        for msg in self.message_list:
            if msg["type"] == "floor_hit" and self.vel.y > 0:
                # constrain y on or above floor
                self.pos.y = msg["y"] - self.radius


class FixedPointMass(PointMass):
    def __init__(self, pos, vel, world, radius=10, mass=10,
                 viscous_damping=0.01, restitution=0.95, drawer=None):
        super().__init__(pos, vel, world, radius, mass,
                         viscous_damping, restitution, drawer)
        self.vel, self.mass = PgVector((0, 0)), 1e9

    def move(self):
        pass


def compute_restoring_force(pos1, pos2, spring_const, natural_len):
    if pos1 == pos2:
        return None
    vector12 = pos2 - pos1
    distance = vector12.magnitude()
    unit_vector12 = vector12 / distance
    f1 = unit_vector12 * spring_const * (distance - natural_len)
    return f1


class Spring:
    def __init__(self, point_mass1, point_mass2, world,
                 spring_const=0.01, natural_len=0, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer

        self.p1 = point_mass1
        self.p2 = point_mass2
        self.spring_const = spring_const
        self.natural_len = natural_len

    def update(self):
        if not (self.p1.is_alive and self.p2.is_alive):
            self.is_alive = False
            return
        self.generate_force()

    def draw(self, screen):
        self.drawer(screen, self.p1.pos, self.p2.pos)

    def generate_force(self):
        f1 = compute_restoring_force(self.p1.pos, self.p2.pos, self.spring_const, self.natural_len)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)


class FragileSpring(Spring):
    def __init__(self, point_mass1, point_mass2, world,
                 spring_const=0.01, natural_len=0, drawer=None,
                 break_threshold=1e9):
        super().__init__(point_mass1, point_mass2, world, spring_const,
                         natural_len, drawer)
        self.break_threshold = break_threshold

    def generate_force(self):
        f1 = compute_restoring_force(self.p1.pos, self.p2.pos, self.spring_const, self.natural_len)
        if f1 is None:
            return
        self.p1.receive_force(f1)
        self.p2.receive_force(-f1)
        if f1.magnitude() > self.break_threshold:
            self.is_alive = False


def is_point_mass(actor):
    return isinstance(actor, PointMass)


def compute_impact_force_between_points(p1, p2, dt):
    if (p1.pos - p2.pos).magnitude() > p1.radius + p2.radius:
        return None
    if p1.pos == p2.pos:
        return None
    normal = (p2.pos - p1.pos).normalize()
    v1 = p1.vel.dot(normal)
    v2 = p2.vel.dot(normal)
    if v1 < v2:
        return None
    e = p1.restitution * p2.restitution
    m1, m2 = p1.mass, p2.mass
    f1 = normal * (-(e + 1) * v1 + (e + 1) * v2) / (1/m1 + 1/m2) / dt
    return f1


class CollisionResolver:
    def __init__(self, world, actor_list, target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer

        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        if self.drawer is not None:
            self.drawer(surface)
            

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = compute_impact_force_between_points(p1, p2, self.world.dt)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)


def compute_impact_force_by_fixture(p, normal, point_included, dt):
    invasion = normal.dot(p.pos - point_included)
    if invasion + p.radius > 0 and normal.dot(p.vel) > 0:
        e = p.restitution
        v = normal.dot(p.vel)
        m = p.mass
        f = normal * (-(e + 1) * v) * m / dt
    else:
        f = None
    return f


class countedCollisionResolver(CollisionResolver):
    def __init__(self, world, actor_list, target_condition=None, drawer=None):
        super().__init__(world, actor_list, target_condition, drawer)
        self.ncolli = 0

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = compute_impact_force_between_points(p1, p2, self.world.dt)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)
                self.ncolli += 1
                
    def draw(self, surface):
        font = pygame.font.Font(None, 50)
        text_image = font.render(str(self.ncolli), True, pygame.Color("white"))
        surface.blit(text_image, (0, 0))
        if self.drawer is not None:
            self.drawer(surface)


class Boundary:
    def __init__(self, normal, point_included, world, actor_list,
                 target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer

        self.normal = PgVector(normal).normalize()
        self.point_included = PgVector(point_included)
        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        if self.drawer is not None:
            self.drawer(surface)

    def is_floor(self):
        return self.normal == PgVector((0, 1))

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        for p in plist:
            f = compute_impact_force_by_fixture(p, self.normal, self.point_included, self.world.dt)
            if f is None:
                continue
            p.receive_force(f)
            if self.is_floor():
                p.receive_message({"type": "floor_hit", "y": self.point_included.y})
                